import sqlite3
import ollama

def load_inflation_data(db_path):
    """Loads all inflation rates from the database into a dictionary"""

    # Connect to the SQLite database and get all years and inflation rates
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT year, inflation_rate FROM inflation_data")

    # Create a dictionary from the results
    data = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return data

def ask_ollama_about_year(year, rate):
    """Send the inflation data to the local LLM (Mistral)"""

    # Creates a prompt for ollama, where we define what we want to know
    prompt = (
        f"The inflation rate in Switzerland in the year {year} was {rate:.2f}%. "
        f"Explain what this means economically in simple terms."
    )

    # Asks the question to the model mistral 
    # Gets a structured json answer with the generated text back
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extracts the answer from the LLM and gives it back as a string
    return response['message']['content']

# ------------------------
# Main Logic
# ------------------------

if __name__ == "__main__":
    db_path = "inflation_ch.db"
    inflation_data = load_inflation_data(db_path)

    # Asks the user for a year which is saved as a int
    year = int(input("Enter a year (2000–2024): "))

    # Checks if year is in the database
    # If yes it asks ollama for this year and receives an answer
    # If not it prints an error message
    if year in inflation_data:
        summary = ask_ollama_about_year(year, inflation_data[year])
        print(f"\nSummary for {year}:\n{summary}")
    else:
        print("Year not found in database.")
