import numpy as np

from dash import html


class RandomGenerator:
    """The RandomGenerator object contains functions used for Random Generator tab"""

    @staticmethod
    def process_result(text, n_items, n_groups, task, style):
        """
        Processing for random generator, selecting or splitting items

        Args:
            text (text): input text
            n_items (int): number of items
            n_groups (int): number of groups
            task (str): task to perform
            style (dict): current style of results div

        Returns:
            3-element tuple

            - (list): div result of result div
            - (list): div result of output div
            - (dict): updated style of output div
        """
        # Initialize return variables
        result = []
        output = [html.H5("Result"), html.Br()]

        # Get list of items
        list_items = text.split("\n")
        np.random.shuffle(list_items)

        # Assertion for number of items
        if task == "item":
            if len(list_items) < n_items:
                result = [f"Error: Too little items to select {n_items} items, please increase number of items or "
                          f"decrease number of groups"]
        elif task == "group":
            if len(list_items) < n_groups:
                result = [f"Error: Too little items to split into {n_groups} groups, please increase number of items"]

        # If no error
        if not result:
            style = {}

            # Perform task accordingly
            if task == "item":
                selection = list(np.random.choice(list_items, n_items, replace=False))
                output_tmp = [html.P("Item(s) selected:", className="p-short p-bold"), html.Br()]
                for idx in range(len(selection)):
                    selection.insert((idx * 2) + 1, html.Br())
                output_tmp += selection
            elif task == "group":
                list_of_array = [list(x) for x in np.array_split(list_items, n_groups)]
                output_tmp = [html.P("Groups:", className="p-short p-bold"), html.Br()]
                for group_idx, group in enumerate(list_of_array):
                    for idx in range(len(group)):
                        group.insert((idx * 2) + 1, html.Br())
                    output_tmp += [html.Br(), html.P(f"Group {group_idx + 1}", className="p-bold")] + group
            output.append(html.P(output_tmp))

        return result, output, style
