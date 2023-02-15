import config
from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config={
    "email": config.email,
    "password": config.password
})


def save_to_text_file(string_to_save):
    with open("output.txt", "w") as file:
        file.write(string_to_save)


def read_text_from_file(text_to_read='input.txt'):
    with open(text_to_read, 'r') as file:
        file_contents = file.read()

    return file_contents


def split_string(text):
    sections = []
    section = ""
    subsection = ""
    lines = text.split("\n")

    for line in lines:
        if not line:
            if len(section.split()) + len(subsection.split()) > config.word_limit:
                sections.append(section)
                section = subsection + "\n"
            else:
                section += subsection + "\n"
            subsection = ""
        else:
            subsection += line + "\n"

    sections.append(section + subsection)
    return sections


def translate(text_sections):
    translation = ""
    for count, section in enumerate(text_sections, start=1):
        print(f"[{count}/{len(text_sections)}]")
        prompt = config.default_prompt + section

        for data in chatbot.ask(
                prompt,
                conversation_id=chatbot.config.get("conversation"),
                parent_id=chatbot.config.get("parent_id"),
        ): pass
        translation += f"{data['message']}\n\n"

    return translation


if __name__ == '__main__':
    input_text = read_text_from_file()
    text_sections = split_string(input_text)
    translated_text = translate(text_sections)
    save_to_text_file(translated_text)
