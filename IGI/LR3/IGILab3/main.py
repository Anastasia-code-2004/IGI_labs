import task1, task2, task3, task4, input
import task5

# Lab work 3 Standard types, collections, modules, functions
# Nikolaychik Anastasia 31.03.2024

if __name__ == '__main__':
    while True:
        choose = input.get_user_choice_main_menu()
        if choose == 0:
            break
        elif choose == 1:
            task1.input_output_decomposition()
        elif choose == 2:
            task2.input_output_even_numbers()
        elif choose == 3:
            task3.input_text_output_punctuation()
        elif choose == 4:
            task4.output_ending_with_consonant()
            task4.average_length()
            task4.print_every_seventh_word()
        elif choose == 5:
            task5.input_process_output()
