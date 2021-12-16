import numpy as np
import pandas as pd

from dash import html

from components.helper import (
    return_message,
    generate_datatable,
    valid_email,
    send_email,
)


class EventPlanner:
    """The EventPlanner object contains functions used for Event Planner tab"""

    @staticmethod
    def process_result(
        df, event, n_groups, pair_flag, criteria_level, email_flag, hide_flag, style
    ):
        """Processing for event planner, shuffling and splitting participants

        Args:
            df (pandas DataFrame): input DataFrame
            event (str): name of event, for result heading and email
            n_groups (int): number of groups
            pair_flag (str): option whether to pair participants up
            criteria_level (str): whether criteria is on individual or group level
            email_flag (str): option whether to email results to recipients
            hide_flag (str): option whether to display output results
            style (dict): current style of results div

        Returns:
            3-element tuple

            - (list): div result of result div
            - (list): div result of output div
            - (dict): updated style of output div
        """
        # Initialize return variables
        result = []
        output = [html.H5(f"Result for {event}"), html.Br()]

        # Get list of people and emails, shuffle and split
        people = list(df[df.columns[0]].dropna().values)
        people_copy = people.copy()
        emails = list(df[df.columns[1]].dropna().values)
        other_cols = list(df.columns[2:])
        other_cols_values = list(list(df[col].dropna().values) for col in other_cols)

        # Assertion for number of participants
        if len(people) <= 1:
            result = [
                "Error: Too little participants, please increase number of participants"
            ]
        elif 2 * n_groups > len(people):
            result = [
                f"Error: Too many groups specified for {len(people)} people, please reduce number of groups"
            ]

        # Assertion for email
        if email_flag:
            n_valid_email = np.sum(valid_email(email) for email in emails)
            if len(people) != n_valid_email:
                result = ["Error: Some emails are not valid, please enter valid emails"]
            if len(people) != len(emails):
                result = [
                    "Error: Number of participants and number of emails do not match"
                ]
        else:
            if hide_flag:
                result = [
                    "Error: Results will not be displayed or emailed to participants, are you sure?"
                ]

        # If no error
        if not result:
            style = {}

            # Shuffle and split into groups
            np.random.shuffle(people_copy)
            list_of_array = np.array_split(people_copy, n_groups)

            # Criteria: if criteria is individual or group level
            if criteria_level == "group":
                criteria_list_tmp = EventPlanner().get_criteria_list(other_cols_values, n=n_groups)
                criteria_list = []
                for idx, group in enumerate(list_of_array):
                    criteria_list.append(np.vstack([list(np.array(criteria_list_tmp)[:, idx])] * len(group)))
                criteria_list = np.vstack(criteria_list).T
            else:
                criteria_list = EventPlanner().get_criteria_list(other_cols_values, n=len(people))
            criteria_df = pd.DataFrame(dict(zip(other_cols, criteria_list)))

            # Matching: shuffle within group
            output_df = pd.DataFrame()
            for idx, group in enumerate(list_of_array):
                # If participants need to pair with each other
                if pair_flag:
                    group_copy = group.copy()
                    shuffle = True
                    while shuffle:
                        np.random.shuffle(group_copy)
                        if np.sum(group == group_copy) == 0:
                            shuffle = False
                    tmp_df = pd.DataFrame({"Group": idx + 1, "Person": group, "Partner": group_copy})
                else:
                    tmp_df = pd.DataFrame({"Group": idx + 1, "Person": group})
                if len(output_df):
                    output_df = output_df.append(tmp_df)
                else:
                    output_df = tmp_df.copy()

            # Join criteria results with matching results
            output_df = output_df.reset_index(drop=True).join(criteria_df)

            if not hide_flag:
                output.append(generate_datatable(output_df, max_rows=len(output_df)))
                output.append(html.Br())
            if email_flag:
                email_dict = dict(zip(people, emails))
                status_code = EventPlanner().email_results(output_df, email_dict, event)
                if status_code:
                    reply = return_message["email_sent_all"]
                else:
                    reply = return_message["email_fail_all"]
                output.append(html.P(reply))

        return result, output, style

    @staticmethod
    def get_criteria_list(other_cols_values, n):
        """Create list of criteria selection for every criteria column

        Args:
            other_cols_values (list): list of criteria columns
            n (int): number of criterias to generate

        Returns:
            (list): list of criteria selection that is randomly selected
        """
        criteria_list = []
        for m in range(len(other_cols_values)):
            criteria = other_cols_values[m]
            np.random.shuffle(criteria)
            if n <= len(criteria):
                criteria_list.append(criteria[:n])
            else:
                criteria_list.append(criteria + list(np.random.choice(criteria, n - len(criteria))))
        return criteria_list

    @staticmethod
    def email_results(output_df, email_dict, event):
        """Function to send email to participants

        Args:
            output_df (pandas DataFrame): output DataFrame from process_result
            email_dict (dict): dictionary mapping participants to email address
            event (str): name of event, for result heading and email

        Returns:
            (bool) indicator if email is sent
        """
        status_code_all = True
        for row_idx, row in output_df.iterrows():
            person = row.Person
            row = row.drop("Person")
            email_body = f"Here are your results for {event}\n\n"
            email_body += "\n".join([f"{k}: {v}" for k, v in row.to_dict().items()])
            email_body += (
                "\n\nThank you for using kayjan.herokuapp.com\n"
                "Disclaimer: This is an automated email. Please do not reply."
            )
            subject = f"{event} Results for {person}"
            recipient = email_dict[person]
            status_code = send_email(email_body, subject=subject, recipient=recipient)
            if not status_code:
                status_code_all = False
        return status_code_all
