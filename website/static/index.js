function unEscape(htmlStr) {
	htmlStr = htmlStr.replace(/&lt;/g, "<");
	htmlStr = htmlStr.replace(/&gt;/g, ">");
	htmlStr = htmlStr.replace(/&quot;/g, '"');
	htmlStr = htmlStr.replace(/&#39;/g, "'");
	htmlStr = htmlStr.replace(/&amp;/g, "&");
	return htmlStr;
}

var stringToHTML = function (str) {
	var parser = new DOMParser();
	var doc = parser.parseFromString(str, "text/html");
	return doc.body;
};

function checkAnswer(answer, problem_id) {
	console.log(problem_id);
	const ansMap = new Map();
	const str = answer.split(",");
	for (let st of str) {
		s = st.split(":");
		ansMap.set(s[0], s[1]);
	}

	for (let i = 0; i < ansMap.size; i++) {
		let doc = document.getElementsByClassName(`list-${i}`)[0];
		if (doc && doc.id != `zone-${ansMap.get(`${i}`)}`) {
			console.log(doc);
			console.log(`zone-${ansMap.get(`${i}`)}`);
			document.getElementById("check").innerHTML = "wrong";
			document.getElementById("check").style.color = "red";
			return;
		}
	}
	var correct = true;
	if (document.getElementById("check").style.color == "red") {
		correct = false;
	}
	console.log("correct");
	fetch("/puzzle-instance", {
		method: "POST",
		body: JSON.stringify({ correct: correct, problem_id: problem_id }),
	}).then((_res) => {
		window.location.href = "/practice";
	});
}

function initDrag(idx) {
	let lists = document.getElementsByClassName("list");
	let zoneBox = [];
	let leftBox = document.getElementById("left");
	for (let i = 0; i < idx; i++) {
		zoneBox[i] = document.getElementById("zone-" + i);
	}
	for (let list of lists) {
		list.addEventListener("dragstart", function (e) {
			let selected = e.target;
			document.getElementById(list.id).style.zIndex = 2;
			list.style.zIndex = 0;
			for (let i = 0; i < zoneBox.length; i++) {
				zoneBox[i].addEventListener("dragenter", function (e) {
					zoneBox[i].classList.add("over");
				});
				zoneBox[i].addEventListener("dragleave", function (e) {
					zoneBox[i].classList.remove("over");
				});
				zoneBox[i].addEventListener("dragover", function (e) {
					console.log(zoneBox[i].id);
					e.preventDefault();
				});
				zoneBox[i].addEventListener("drop", function (e) {
					zoneBox[i].appendChild(selected);
					zoneBox[i].style.zIndex = 1;
					list.style.zIndex = 2;
					list.id = "zone-" + i;
					selected = null;
				});
			}
			leftBox.addEventListener("dragover", function (e) {
				e.preventDefault();
			});
			leftBox.addEventListener("drop", function (e) {
				leftBox.appendChild(selected);
				list.id = "n/a";
				selected = null;
			});
		});
		list.addEventListener("dragend", function (e) {
			for (let i = 0; i < zoneBox.length; i++) {
				zoneBox[i].classList.remove("over");
			}
		});
	}
}

/* When the user clicks on the button,
			toggle between hiding and showing the dropdown content */
function myFunction() {
	document.getElementById("myDropdown").classList.toggle("show");
}

function filterSearch() {
	var input, filter, ul, li, a, i;
	input = document.getElementById("myInput");
	filter = input.value.toUpperCase();
	div = document.getElementById("list1");
	a = div.getElementsByTagName("li");
	for (i = 0; i < a.length; i++) {
		txtValue = a[i].textContent || a[i].innerText;
		if (txtValue.toUpperCase().indexOf(filter) > -1) {
			a[i].style.display = "";
		} else {
			a[i].style.display = "none";
		}
	}
}

function filterTable() {
	size = document.getElementsByClassName("tag").length;
	check_tags = [];
	for (let i = 0; i < size; i++) {
		if (document.getElementsByClassName("tag")[i].checked) {
			check_tags.push(document.getElementsByClassName("tag")[i].value);
		}
	}
	console.log(check_tags);
	fetch("/filter-dashboard", {
		method: "POST",
		body: JSON.stringify({ tags: check_tags }),
	}).then((_res) => {
		window.location.href = "/dashboard";
	});
}

function filterProblem() {
	size = document.getElementsByClassName("tag").length;
	check_tags = [];
	for (let i = 0; i < size; i++) {
		if (document.getElementsByClassName("tag")[i].checked) {
			check_tags.push(document.getElementsByClassName("tag")[i].value);
		}
	}
	console.log(check_tags);
	fetch("/filter-problem", {
		method: "POST",
		body: JSON.stringify({ tags: check_tags }),
	}).then((_res) => {
		window.location.href = "/practice";
	});
}

function initCheckList(checkedTags) {
	var checkList = document.getElementById("list1");
	checkList.getElementsByClassName("anchor")[0].onclick = function (evt) {
		if (checkList.classList.contains("visible"))
			checkList.classList.remove("visible");
		else checkList.classList.add("visible");
	};
	tags = checkedTags.split(',');
	size = document.getElementsByClassName("tag").length;
	for (let i = 0; i < size; i++) {
		if (tags.includes(document.getElementsByClassName("tag")[i].value)) {
			console.log("g")
			document.getElementsByClassName("tag")[i].checked = true;
		}
	}
}
