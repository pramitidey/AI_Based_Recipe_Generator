import streamlit as st
import requests
import pandas as pd
def call_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",  
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"
API_BASE_URL = "http://127.0.0.1:8000"  
st.set_page_config(page_title="AI Recipe Finder", layout="wide", page_icon="🍴")
def get_user_preferences():
    st.subheader("Personalized Recipe Preferences")
    diet = st.selectbox("Select your dietary preference:", ["None", "Vegetarian", "Vegan", "Keto", "Gluten-Free"])
    allergies = st.text_input("List any allergies (comma separated):")
    ingredients = st.text_area("Available ingredients (comma separated):")
    cuisine = st.selectbox("Preferred cuisine:", ["Any", "Indian", "Italian", "Chinese", "Mexican", "American"])
    return diet, allergies, ingredients, cuisine
def generate_prompt(diet, allergies, ingredients, cuisine):
    prompt = f"You're an expert chef. Generate a creative and unique recipe using the following ingredients: {ingredients}.\n"
    if diet != "None":
        prompt += f"The recipe must be {diet.lower()}.\n"
    if allergies:
        prompt += f"Avoid the following allergens: {allergies}.\n"
    if cuisine != "Any":
        prompt += f"The recipe should reflect {cuisine} cuisine.\n"
    prompt += "Include a recipe name, ingredients list, and step-by-step instructions."
    return prompt
def display_generated_recipe(recipe_text):
    st.subheader("🧑‍🍳 Here's Your AI-Generated Recipe!")
    st.markdown(recipe_text)
    st.download_button("Download Recipe", recipe_text, file_name="ai_recipe.txt")
st.header("AI Custom Recipe Generator")
diet, allergies, ingredients, cuisine = get_user_preferences()
if st.button("Generate AI Recipe"):
    if not ingredients.strip():
        st.warning("Please provide some ingredients.")
    else:
        with st.spinner("Cooking up your custom recipe..."):
            prompt = generate_prompt(diet, allergies, ingredients, cuisine)
            recipe = call_llm(prompt)
            display_generated_recipe(recipe)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://4kwallpapers.com/images/wallpapers/ios-13-stock-ipados-dark-green-black-background-amoled-ipad-2560x1440-794.jpg");
        background-attachment: fixed;
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
)