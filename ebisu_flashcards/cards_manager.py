import sqlite3
import ebisu
import datetime

def get_time_from_review(fact):
    try: 
        now = datetime.datetime.now()
        last_review_time = datetime.datetime.strptime(fact["lastreview"], "%Y-%m-%d %H:%M:%S")
        time_from_review = now - last_review_time / datetime.timedelta(hours=1)
    except Exception:
        time_from_review = 1
    return time_from_review

def compute_probability(fact):
    prob = ebisu.predictRecall(
                (fact["alpha"], fact["beta"], fact["t"]),
                get_time_from_review(fact))
    print(prob*-100, fact["question"])
    return prob
    
def main():
    # CREATE TABLE facts (id int, question text, answer text, alpha real, beta real, t real, lastreview text)

    # Connect to DB and load all data in memory
    conn = sqlite3.connect("ebisu-facts.db") 
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from facts order by lastreview")
    facts = [dict(row) for row in c.fetchall()]
        
    # Loop and ask questions
    while True:
        # Select the fact most likely to be forgotten
        # FIXME you just need the max actually
        facts = sorted(facts, key=lambda fact: compute_probability(fact))
        selected_fact = facts.pop(0)
                
        # Ask the user
        answer = input("Question (prob: {:.2f}): {} ->  ".format(compute_probability(selected_fact)*-100, selected_fact["question"]))

        # Update model for this fact
        success = 1 if answer == selected_fact["answer"] else 0
        now_iso = datetime.datetime.now().isoformat()
        
        alpha, beta, t = ebisu.updateRecall((selected_fact["alpha"], selected_fact["beta"], selected_fact["t"]), success, 1, get_time_from_review(selected_fact))
        
        # Update list
        
        selected_fact["alpha"] = alpha
        selected_fact["beta"] = beta
        selected_fact["t"] = t
        facts.append(selected_fact)
        
        if success:
            print("Good job!")
        else:
            print("Nope... the answer was '{}'.".format(selected_fact["answer"]))
            
        if input("Wanna continue? (y/n)").lower() != "y":
            print("Ok, bye!")  

            for fact in facts:
                c.execute("""update facts set alpha = {}, beta = {}, t = {}, lastreview = '{}' where id = {}""".format(fact["alpha"], fact["beta"], fact["t"], fact["lastreview"], fact["id"]))
            conn.commit()
            conn.close()    
            break


if __name__ == "__main__":
    main()
