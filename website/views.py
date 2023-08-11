from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy.sql import func
from sqlalchemy import select, or_
from flask_login import login_required, current_user
from .models import User, Problem, ProblemInstance
from . import db
import json, html, random


views = Blueprint('views', __name__)

filter_tags_dash = set()
filter_tags_practice = set()

class Problem_Variation:
    def __init__(self, problem_id, problem_name, tags, difficulty, description, code, options, answer) -> None:
        self.id = problem_id
        self.problem_name = problem_name
        self.tags = tags.rstrip(",")
        self.difficulty = difficulty
        self.description = description
        self.code = code
        self.options = options
        self.answer = answer

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    filter_tags_dash.clear()
    return render_template("home.html", user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # query all tags from users completed problems
    tags_query = (
    db.session.query(ProblemInstance)
    .join(Problem)
    .with_entities(Problem.tags)
    .filter(ProblemInstance.user_id == current_user.id)
    )

    # Execute the query and fetch the instances
    matching_instances = tags_query.distinct()
    all_tags = set() 
    for instance in matching_instances:
        tags = instance.tags.split(',') 
        all_tags.update(tags)  # Add the tags to the set
    all_tags.discard('')
    # if no tags selected to filter, show all problems
    if len(filter_tags_dash) == 0:
        tags = all_tags
    else:
        tags = filter_tags_dash
    # Query for problems from the user's ProblemInstances that match the provided tags 
    instances_query = (
        db.session.query(ProblemInstance)
        .filter(ProblemInstance.user_id == current_user.id)
        .join(Problem, Problem.id == ProblemInstance.problem_id)
        .filter(or_(*[Problem.tags.like("%"+tag+"%") for tag in tags]))
        .order_by(ProblemInstance.date.desc())
    )
    problems = instances_query.all()

    # set current filter
    cur_filter = ""
    for t in filter_tags_dash:
        cur_filter += t + ','
    cur_filter = cur_filter.strip(',')
    
    return render_template("dashboard.html", user=current_user, problem_tags=all_tags, problems=problems, cur_filter=cur_filter)

@views.route('/filter-dashboard', methods=['POST'])
@login_required
def dashboardFiltered():
    # get checked tags and update
    given_tags = json.loads(request.data)
    filter_tags_dash.clear()
    filter_tags_dash.update(given_tags['tags'])

    return jsonify({})

@views.route('/practice', methods=['GET', 'POST'])
@login_required
def practice():
    filter_tags_dash.clear()

    # query all tags from all problems
    tags_query = (
    db.session.query(Problem)
    .with_entities(Problem.tags)
    )
    # Execute the query and fetch the instances
    matching_instances = tags_query.distinct()
    all_tags = set() 
    for instance in matching_instances:
        tags = instance.tags.split(',') 
        all_tags.update(tags)  # Add the tags to the set 
    all_tags.discard('')
    
    # if no tag filter selected, choose any problem
    if len(filter_tags_practice) == 0:
        tags = all_tags
    else:
        tags = filter_tags_practice

    # query problem with tags filter and pick random
    instances_query = (
        db.session.query(Problem)
        .filter(or_(*[Problem.tags.like("%"+tag+"%") for tag in tags]))  
    )
    problem_query = instances_query.order_by(func.random()).first()

    # problem_name, tags, difficulty, description, code, options, answer
    problem_id = problem_query.id
    problem_name = problem_query.problem_name
    tags = problem_query.tags
    difficulty = problem_query.difficulty
    description = problem_query.description
    code = problem_query.code

    code_lines = code.split("$")

    # choose random lines for options 
    if len(code_lines) < 7: 
        opt = random.sample(list(range(2, len(code_lines)-1)), len(code_lines)//3) 
    else:
        opt = random.sample(list(range(2, len(code_lines)-1)), 4)
    options = [[] for i in range(len(opt))]
    # answers is map of option to zone
    answers = {}
    total_zones = 0
    code = []
    option_chosen = 0

    # iterate through each line of code
    line_idx = 0
    while line_idx < len(code_lines):
        # each span is '@' del
        spans = code_lines[line_idx].split("@")
        # if line was chosen as option,
        #  add to options, find number of zones, add to answer
        if line_idx in opt:
            # make sure line has substance, else choose other random lines
            if len(spans) < 5:
                opt = random.sample(list(range(line_idx+1, len(code_lines)-1)), 4-option_chosen)
                continue
            for spans_idx in range(0, len(spans), 2):
                # text is even, class is odd
                options[option_chosen].append([spans[spans_idx].replace(u'\xa0', ''), spans[spans_idx+1]])
            # new_zones is (indent amount / 4) - 1 for not zone in first indent
            new_zones = int(len(spans[0])/4) - 1
            total_zones += new_zones
            # map option to zone - 1 for zero index zone
            answers[option_chosen] = total_zones-1
            total_zones += 1
            # append code line with no spans to indicate zones
            code.append(f"{new_zones+1}")
            option_chosen += 1
        else:
            code.append([])
            # add all spans in line to code
            for spans_idx in range(0, len(spans)-1, 2):
                code[line_idx].append([spans[spans_idx], spans[spans_idx+1]])
        line_idx += 1
    # change answermap to str
    answer = ""
    for key,val in answers.items():
        answer += f"{key}:{val},"
    answer = answer.strip(",")
    # pass attributes to problem obj to pass to template
    problem = Problem_Variation(problem_id, problem_name, tags, difficulty, description, code, options, answer)       

    # set current filter used
    cur_filter = ""
    for t in filter_tags_practice:
        cur_filter += t + ','
    cur_filter = cur_filter.strip(',')

    return render_template("practice.html", user=current_user, cur_filter=cur_filter, problem_tags=all_tags, problem=problem)

@views.route('/filter-problem', methods=['POST'])
@login_required
def practiceFiltered():
    # update filter tags for practice page
    given_tags = json.loads(request.data)
    filter_tags_practice.clear()
    filter_tags_practice.update(given_tags['tags'])

    return jsonify({})

@views.route('/puzzle-instance', methods=['POST'])
def check_puzzle():
    # get puzzle once solved and send to problem_instance table
    correct = json.loads(request.data)
    prob = Problem.query.get(correct['problem_id'])
    prob_inst = ProblemInstance(user_id=current_user.id, problem_id=prob.id, problem_name=prob.problem_name)
    if correct:
        prob_inst.correct = correct['correct']
    db.session.add(prob_inst)
    db.session.commit()
    return jsonify({})    
