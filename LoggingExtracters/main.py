import re
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_logs(log_file):
    """Extract error messages from a log file and return as a DataFrame."""
    error_pattern = re.compile(r"ERROR: (.+)")
    errors = []

    with open(log_file, "r") as file:
        for line in file:
            match = error_pattern.search(line)
            if match:
                errors.append({"Timestamp": line[:19], "Error": match.group(1)})

    # df = pd.DataFrame(errors)

    df = pd.DataFrame(errors)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df
    # return df

def generate_summary(df):
    """Generate a summary of error occurrences."""
    summary = df["Error"].value_counts().reset_index()
    summary.columns = ["Error Message", "Count"]
    return summary


def generate_time_based_trends(df):
    """Generate time-based error trends."""
    df.set_index("Timestamp", inplace=True)

    # Errors per hour
    errors_per_hour = df.resample('H').size().reset_index(name='Count')

    # Errors per day
    errors_per_day = df.resample('D').size().reset_index(name='Count')

    return errors_per_hour, errors_per_day

def main(log_file):
    logging.info(f"Processing log file: {log_file}")

    df = parse_logs(log_file)
    if df.empty:
        logging.info("No errors found.")
        return

    summary = generate_summary(df)

    # Save results
    df.to_csv("error_logs.csv", index=False)
    summary.to_csv("error_summary.csv", index=False)

    logging.info("Log analysis complete. Results saved.")

    df.to_csv("error_logs.csv", index=False)
    summary.to_csv("error_summary.csv", index=False)

    errors_per_hour, errors_per_day = generate_time_based_trends(df)
    errors_per_hour.to_csv("errors_per_hour.csv", index=False)
    errors_per_day.to_csv("errors_per_day.csv", index=False)

    logging.info("Log analysis complete. Results saved.")

if __name__ == "__main__":
    log_file = "system_logs.txt"  # Change this to your log file
    main(log_file)
