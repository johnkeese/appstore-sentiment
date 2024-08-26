import pandas as pd
import openai

# Set your OpenAI API key here
openai.api_key = 'REPLACE_WITH_YOUR_KEY'


def process_reviews():
    # Read the CSV file with the correct encoding
    df = pd.read_csv('app_store_reviews.csv', encoding='utf-8-sig')

    # Apply sentiment analysis, feature delight, and feature need to each Title + Review
    df['Title_and_Review'] = df['Title'] + " " + df['Review']
    print("Calculating sentiment...")
    df['Sentiment'] = df['Title_and_Review'].apply(get_sentiment)
    print("Sentiment completed. Finding feature needs...")
    df['Need'] = df['Title_and_Review'].apply(get_feature_need)
    print("Finding features completed.")

    # TO DO: This prompt consistently failed to produce content differing from get_feature_need
    # df['Delight'] = df['Title_and_Review'].apply(get_feature_delight)

    # Save the result to a new CSV file with the correct encoding
    df.to_csv('app_store_reviews_with_sentiment.csv',
              index=False,
              encoding='utf-8-sig')

    print(
        "Sentiment analysis complete. The results are saved in 'app_store_reviews_with_sentiment.csv'."
    )


# Get the generic sentiment about review from ChatGPT
def get_sentiment(review_text):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{
            "role": "system",
            "content": "You are a sentiment analyst expert."
        }, {
            "role":
            "user",
            "content":
            f"Evaluate the following statement: '{review_text}' Respond only with a number from 0 to 100 where 0 is if the sentiment of this statement is fully negative and 100 if the sentiment is fully positive."
        }])

    # Catch an error if for some reason GPT decides to respond with text
    try:
        return int(response.choices[0].message.content.strip())
    except (ValueError, TypeError) as e:
        return 51  # TO DO: Kind of a lame default, should probably improve


# TO DO: This prompt consistently failed to produce content differing from get_feature_need
def get_feature_delight(review_text):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{
            "role":
            "system",
            "content":
            "You are a digital product manager expert and are excellent at looking at customer statements and understanding if there is a feature that caused delight and enjoyment in your product. Your task is to evaluate customer statements and determine if there is a feature in your product that should be enhanced or iterated to create an even better customer experience. Respond only with your finding. If there is no feature identified, respond with 'n/a'."
        }, {
            "role": "user",
            "content": review_text
        }])

    return response.choices[0].message.content.strip()


def get_feature_need(review_text):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{
            "role":
            "system",
            "content":
            "You are a digital product manager expert and are excellent at looking at customer statements and understanding if there is a feature need in your product. Perhaps the feature is missing or could be better. Your task is to evaluate customer statements and determine if there is a feature in your product that should be added or changed to create an even better customer experience. Respond only with your finding. If there is no feature identified, respond with 'n/a'."
        }, {
            "role": "user",
            "content": review_text
        }])

    return response.choices[0].message.content.strip()
