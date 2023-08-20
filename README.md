
# AlgDash - http://sninic2.pythonanywhere.com/

AlgDash is a web application crafted to offer users a more streamlined approach to honing their skills for technical interviews. While it doesn't aim to supplant platforms like LeetCode, its purpose is to complement them. AlgDash serves as an invaluable companion, particularly in situations where executing complete coded solutions might be impractical – think of it as your go-to resource for practicing on the fly or during time-constrained scenarios. Through its intuitive drag-and-drop interface, AlgDash empowers users to engage in numerous iterations of problem-solving, facilitating rapid comprehension of prompts and fostering enhanced practice.


## Website Usage

Up to this point, accessing the web application mandates user authentication through either login or new account creation. Upon successful authentication, users will be seamlessly ushered to the home page. The home page will provide comprehensive, high-level information, whereas the dashboard will be tailored to individual user performance, ensuring a personalized experience. For active practice sessions, the practice page stands ready to be utilized. Puzzles are intelligently categorized with tags corresponding to the specific topics they cover, thereby allowing users to filter and select problems that align with their focus.

### Drag and Drop

The practice page is where you work on problems. There's a description of the problem on the left, pieces of code you can drag and drop in the middle, and a partially written code on the right. To solve the puzzle, you need to put the code pieces in the right places in the incomplete code, making sure it's indented correctly. After you're done, you can check if your solution is right. If it's right on the first try, you get points. If not, you need to finish it, but you won't get points for the first try.
## Code Usage

To use this code locally:
1. Clone github repo to machine
2. Open \_\_init__.py and change initialization of database to perferred connection
- Make sure that database is defined correctly and configured on corresponding server
3. Open terminal and navigate to project folder, run command - "pip install -r requirements.txt" 
4. In same terminal, run command "python main.py"
#
Backend:
- Flask
- Sqlachemy
Frontend:
- Html/CSS/Javascript
- Bootstrap
Database:
- mysql
