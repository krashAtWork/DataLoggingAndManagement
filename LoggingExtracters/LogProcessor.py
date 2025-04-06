import re
import pandas as pd
import logging
import matplotlib.pyplot as plt


class LogProcessor:

    def __init__(self, sp):
        self.system_logs_path = sp
        self.errorsDF = pd.DataFrame()
        self.error_logs_path = ""
        self.error_summary = pd.DataFrame()
        self.errors_per_day = ""
        self.errors_per_hour = pd.DataFrame()

    def parse_logs(self):
        """Extract error messages from a log file and return as a DataFrame."""
        error_pattern = re.compile(r"ERROR: (.+)")
        errors = []

        with open(self.system_logs_path, "r") as file:
            for line in file:
                match = error_pattern.search(line)
                if match:
                    errors.append({"Timestamp": line[:19], "Error": match.group(1)})
        df = pd.DataFrame(errors)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        print("***************************")
        return df
        # return df

    def get_error_logs(self):
        """
        Get error logs from system logs
        :return: error lines dataframe
        """
        self.errorsDF = self.parse_logs()
        # df = parse_logs(log_file)
        if self.errorsDF.empty:
            logging.info("No errors found.")
            return
        # summary = generate_summary(df)
        # Save results
        self.errorsDF.to_csv("error_logs.csv", index=False)
        # df = pd.read_csv(file_path)
        print("***************************")
        print(self.errorsDF.head())  # Display the first few rows of the dataframe

    def get_error_summary(self):
        """
        Get error summary- error types and count
        """
        self.error_summary = self.errorsDF["Error"].value_counts().reset_index()
        self.error_summary.columns = ["Error Message", "Count"]
        self.error_summary.to_csv("error_summary.csv", index=False)
        print("***************************")
        print(self.error_summary.head())

    def get_error_plot(self):
        # Create a bar graph
        # plt.figure(figsize=(10, 6))
        # plt.bar(self.error_summary["Error Message"], self.error_summary["Count"], color='skyblue')
        # plt.xlabel('Error Message')
        # plt.ylabel('Count')
        # plt.title('Error Messages Count')
        # plt.xticks(rotation=45, ha='right')
        # plt.tight_layout()
        #
        # # Show the plot
        # plt.show()
        #
        print(self.errorsDF)
        self.errorsDF.set_index("Timestamp", inplace=True)

        # # Errors per hour
        self.errors_per_hour = self.errorsDF.resample('h').size().reset_index(name='Count')
        print(self.errors_per_hour)
        # # Create a bar graph
        # plt.figure(figsize=(10, 6))
        # plt.bar(self.errors_per_hour["Timestamp"], self.error_summary["Count"], color='skyblue')
        # plt.xlabel('Hr')
        # plt.ylabel('Count')
        # plt.title('Error  Count / Hr')
        # plt.xticks(rotation=45, ha='right')
        # plt.tight_layout()
        #
        # # Show the plot
        # plt.show()

        # Create a figure with two subplots
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        # First bar plot
        axs[0].bar(self.error_summary["Error Message"], self.error_summary["Count"], color='skyblue')
        axs[0].set_title('Error Messages Types and Count')
        axs[0].set_xlabel('Error Message')
        axs[0].set_ylabel('Count')
        axs[0].set_xticklabels(self.error_summary["Error Message"], rotation=45, ha='right')

        # Second bar plot

        # Convert the 'Timestamp' column to datetime
        self.errors_per_hour['Timestamp'] = pd.to_datetime(self.errors_per_hour['Timestamp'])

        # Extract the hour from the 'Timestamp' column
        self.errors_per_hour['Hour'] = self.errors_per_hour['Timestamp'].dt.hour

        # Group by hour and sum the counts
        hourly_counts = self.errors_per_hour.groupby('Hour')['Count'].sum().reset_index()

        axs[1].bar(hourly_counts['Hour'], hourly_counts['Count'], color='skyblue')
        axs[1].set_title('Error Messages By Hr')
        axs[1].set_xlabel('Hour of the Day')
        axs[1].set_ylabel('Count')
        # axs[1].set_xticklabels(self.errors_per_hour["Error Message"], rotation=45, ha='right')

        # Adjust layout
        plt.tight_layout()

        # Show the plots
        plt.show()
