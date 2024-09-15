from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

class Flashcard(Base):
    __tablename__ = 'flashcard.db'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer, default=1)

Base.metadata.create_all(engine)

def get_non_empty_input(prompt):
    while True:
        print(prompt)
        value = input()
        if not value.isspace() and value:
            return value

def update_flashcard(item):
    new_question = get_non_empty_input(f'current question: {item.question}\nplease write a new question: ')
    item.question = new_question
    new_answer = get_non_empty_input(f'current answer: {item.answer}\nplease write a new answer: ')
    item.answer = new_answer
    session.commit()

while True:
    print('1. Add flashcards')
    print('2. Practice flashcards')
    print('3. Exit')
    choice = input()

    if choice == '1':
        while True:
            print('1. Add a new flashcard')
            print('2. Exit')
            new_choice = input()
            if new_choice == '1':
                quest = get_non_empty_input('Question:')
                ans = get_non_empty_input('Answer:')
                flashcard_data = Flashcard(question=quest, answer=ans)
                session.add(flashcard_data)
                session.commit()
            elif new_choice == '2':
                break
            else:
                print(f'{new_choice} is not an option')

    elif choice == '2':
        flashcards = session.query(Flashcard).all()
        while True:
            if flashcards:
                for item in flashcards:
                    print(f'Question: {item.question}')
                    print('press "y" to see the answer:')
                    print('press "n" to skip:')
                    print('press "u" to update:')
                    new_choice = input()
                    if new_choice == 'y':
                        print(f'Answer: {item.answer}')
                        print('press "y" if your answer is correct:')
                        print('press "n" if your answer is wrong:')
                        is_correct = input()
                        if is_correct == 'y':
                            item.box_number += 1
                            if item.box_number == 3:
                                session.delete(item)
                                session.commit()
                        if is_correct == 'n':
                            if item.box_number > 1:
                                item.box_number -= 1
                            else:
                                pass
                    elif new_choice == 'n':
                        pass
                    elif new_choice == 'u':
                        print('press "d" to delete the flashcard:')
                        print('press "e" to edit the flashcard:')
                        second_choice = input()
                        if second_choice == 'd':
                            session.delete(item)
                            session.commit()
                        elif second_choice == 'e':
                            update_flashcard(item)
                        else:
                            print(f'{second_choice} is not an option')
                    else:
                        print(f'{new_choice} is not an option')
            else:
                print('There is no flashcard to practice!')
            break
    elif choice == '3':
        print('Bye!')
        break
    else:
        print(f'{choice} is not an option')


