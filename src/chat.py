from search import search_prompt

def main():
    #chain = search_prompt()

    #if not chain:
    #    print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
    #    return

    print("Chat pronto. Faça sua pergunta ou digite 'sair' para terminar.")

    while True:
        try:
            question = input("> ")
            if question.lower() == "sair":
                break
            if not question.strip():
                print("Pergunta não pode ser vazia.")
                continue
            search_prompt(question)

        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando o chat.")
            break


if __name__ == "__main__":
    main()
