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

            # Shuffle and split into groups, then shuffle within group
            np.random.shuffle(people_copy)
            list_of_array = np.array_split(people_copy, n_groups)
            output_df = pd.DataFrame()
            for idx, group in enumerate(list_of_array):
                # If criteria is individual or group level
                if criteria_level == "group":
                    criteria_list = EventPlanner().get_criteria_list(other_cols_values)
                else:
                    criteria_list = [
                        EventPlanner().get_criteria_list(other_cols_values)
                        for _ in range(len(group))
                    ]
                # If participants need to pair with each other
                if pair_flag:
                    group_copy = group.copy()
                    shuffle = True
                    while shuffle:
                        np.random.shuffle(group_copy)
                        if np.sum(group == group_copy) == 0:
                            shuffle = False
                    tmp_df = pd.DataFrame(
                        dict(
                            {"Group": idx + 1, "Person": group, "Partner": group_copy},
                            **dict(zip(other_cols, np.array(criteria_list).T)),
                        )
                    )
                else:
                    tmp_df = pd.DataFrame(
                        dict(
                            {"Group": idx + 1, "Person": group},
                            **dict(zip(other_cols, np.array(criteria_list).T)),
                        )
                    )
                if len(output_df):
                    output_df = output_df.append(tmp_df)
                else:
                    output_df = tmp_df.copy()

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
    def get_criteria_list(other_cols_values):
        """Create list of criteria selection for every criteria column

        Args:
            other_cols_values (list): list of criteria columns

        Returns:
            (list): list of criteria selection that is randomly selected
        """
        criteria_list = []
        for m in range(len(other_cols_values)):
            criteria_list.append(np.random.choice(other_cols_values[m]))
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
