import json

def extract_description_words(weights_dict):
    description_words = set()
    
    for position, categories in weights_dict.items():
        for category in categories.keys():
            description_words.add(category)
    
    return sorted(description_words)

def main():
    # Load the weights dictionary
    weights_file_path = 'backend/weights_dict.json'
    with open(weights_file_path, 'r', encoding='utf-8') as file:
        weights_dict = json.load(file)
    
    # Extract and list all the key player description words
    description_words = extract_description_words(weights_dict)
    print("Key player description words:")
    for word in description_words:
        print(word)

if __name__ == "__main__":
    main()