import dash_html_components as html
import numpy as np
import pandas as pd

from components.helper import (
    return_message,
    generate_datatable,
    valid_email,
    send_email,
)


class Santa:
    """The Santa object contains functions used for Secret Santa tab"""

    @staticmethod
    def process_result(df, n_groups, email_flag, hide_flag, style):
        """
        Processing for secret santa, shuffling and splitting participants

        Args:
            df (pandas DataFrame): input DataFrame
            n_groups (int): number of groups
            email_flag (str): option whether to email results to recipients
            hide_flag (str): option whether to display output results
            style (dict): current style of results div

        Returns:
            3-element tuple

            - (list): div result of secret santa upload result
            - (list): updated content of output div
            - (dict): updated style of results div
        """
        # Initialize return variables
        result = []
        output = [html.H5("Result"), html.Br()]

        # Get first column (people), shuffle and split
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
            if len(people) != len(emails):
                result = [
                    "Error: Number of participants and number of emails do not match"
                ]
            n_valid_email = np.sum(valid_email(email) for email in emails)
            if len(people) != n_valid_email:
                result = ["Error: Some emails are not valid, please enter valid emails"]
        else:
            if hide_flag:
                result = [
                    "Error: Results will not be displayed or emailed to participants, are you sure?"
                ]

        if not result:
            style = {}

            # Shuffle and split into groups, then shuffle within group
            np.random.shuffle(people_copy)
            list_of_array = np.array_split(people_copy, n_groups)
            list_of_list = []
            for idx, group in enumerate(list_of_array):
                group_copy = group.copy()
                shuffle = True
                while shuffle:
                    np.random.shuffle(group_copy)
                    if np.sum(group == group_copy) == 0:
                        shuffle = False
                for n in range(len(group)):
                    participant_list = [idx, group[n], group_copy[n]]
                    for m in range(len(other_cols)):
                        participant_list.append(np.random.choice(other_cols_values[m]))
                    list_of_list.append(participant_list)
            output_df = pd.DataFrame(
                list_of_list, columns=["Group", "Person", "Partner"] + other_cols
            )

            if not hide_flag:
                output.append(generate_datatable(output_df, max_rows=len(output_df)))
                output.append(html.Br())
            if email_flag:
                email_dict = dict(zip(people, emails))
                status_code = Santa().email_results(output_df, email_dict)
                if status_code:
                    reply = return_message["email_sent_all"]
                else:
                    reply = return_message["email_fail_all"]
                output.append(html.P(reply))

        return result, output, style

    @staticmethod
    def email_results(output_df, email_dict):
        """
        Function to send email to participants

        Args:
            output_df (pandas DataFrame): output DataFrame from process_result
            email_dict (dict): dictionary mapping participants to email address

        Returns:
            (bool) Status code of email sending
        """
        status_code_all = True
        for row_idx, row in output_df.iterrows():
            person = row.Person
            row = row.drop("Person")
            email_body = "Here are your results for Secret Santa\n\n"
            email_body += "\n".join([f"{k}: {v}" for k, v in row.to_dict().items()])
            email_body += (
                "\n\nThank you for using kayjan.herokuapp.com\n"
                "Disclaimer: This is an automated email. Please do not reply."
            )
            subject = f"Secret Santa Sorting Results for {person}"
            recipient = email_dict[person]
            status_code = send_email(email_body, subject=subject, recipient=recipient)
            if not status_code:
                status_code_all = False
        return status_code_all
