from sentiment import process_reviews
from raw_reviews import get_raw_reviews

def main():
  # Get the app store ID from the user
  input_app_id = input("Enter the App ID from App Store: ") or "431156417"

  # Get the number of review pages to get (50 results per page)
  input_page_num = int(input("How many pages of results do you want? (50 reviews per page): ") or 1)
  
  # Call the function to process reviews
  get_raw_reviews(app_id=input_app_id, num_pages=input_page_num)  # Adjust app_id and num_pages as needed

  # Call the function to process reviews
  process_reviews()

if __name__ == "__main__":
  main()