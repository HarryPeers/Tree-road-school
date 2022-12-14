var login_error = document.getElementById("login-error");
var login_page = document.getElementById("login-page");
var home_page = document.getElementById("home-page");

const pages = [
    ["login-page",null],
    ["home-page",null],
    ["create-page",null],
    ["display-page",get_all_students],
    ["report-page",null],
    ["view-page",null],
    ["reportView-page"]
]

const home_button = document.getElementById("home-button");

function request(method, path, json=null) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open(method, `http://127.0.0.1:80${path}`, false);
    xmlHttp.setRequestHeader("Authentication", localStorage.getItem("password"));
    xmlHttp.send(JSON.stringify(json));
    return [xmlHttp.status, JSON.parse(xmlHttp.responseText)]
}

function login(password) {
    login_error.style.display = "none";
    
    var password = document.getElementById(password).value;

    localStorage.setItem("password", password)
     
    let rsp = request("POST", "/api/login/", null);
    
    if (rsp[1].success) {
        open_page("home");
    } else {
        login_error.style.display = 'block';
    }
}

function open_page(page) {
    pages.forEach((p)=> {
        document.getElementById(p[0]).style.display = "none";
        if (p[1] != null && p[0].startsWith(page)) {
            p[1]();
        }
    })
    
    document.getElementById(`${page}-page`).style.display = "block";
    
    if (!(page == "home" || page == "login")) {
        home_button.style.display = "block";
    } else {
        home_button.style.display = "none";
    }
}

function get_value(id) {
    return document.getElementById(id).value
}

function fill_value(id, value) {
    console.log(id)
    document.getElementById(id).innerHTML = value;
}

function create_student() {
    let payload = {
        "forename": get_value("createStudentForename"),
        "surname": get_value("createStudentSurname"),
        "gender": get_value("createStudentGender"),
        "dob": get_value("createStudentDOB"),
        "address": get_value("createHomeAddress"),
        "number": get_value("createHomeNumber"),
        "group": get_value("createStudentGroup")
    };
    
    let rsp = request("POST", "/api/student/create/", payload);
    
    view_student(rsp[1].id)
};

function view_student(id) {
    open_page("view");
    let rsp = request("GET", `/api/student/view/?student=${id}`, null)
    
    fill_value("viewStudentForename", rsp[1].forename)
    fill_value("viewStudentSurname", rsp[1].surname)
    fill_value("viewStudentGender", rsp[1].gender)
    fill_value("viewStudentDOB", rsp[1].dob)
    fill_value("viewHomeAddress", rsp[1].address)
    fill_value("viewHomeNumber", rsp[1].number)
    fill_value("viewStudentGroup", rsp[1].group)
    fill_value("viewStudentEmail", rsp[1].email)
    fill_value("viewStudentId", id)

    document.getElementById("deleteStudent").onclick = (ev) => {delete_student(id)}
    
}

function delete_student(id) {
    request("POST", `/api/student/delete/?student=${id}`, null)
    open_page("home")
}

function get_all_students() {
    let rsp = request("GET", "/api/student/all/", null)
    var studentTables = document.getElementById('studentTables')
    
    studentTables.innerHTML = `<tr class="first"><th>Forename</th><th>Surname</th><th>Tutor group</th><th>Student id</th></tr>`
    
    rsp[1].students.forEach((student)=>{
        studentTables.innerHTML += `<tr onclick="view_student(${student.id})"><th>${student.forename}</th><th>${student.surname}</th><th>${student.group}</th><th>${student.id}</th></tr>`
    });
}

function open_report(generate) {
    var rsp = request("GET", `/api/reports/${generate}`, null)
    open_page("reportView")
    
    document.getElementById("reportHeader").innerHTML = generate;
    
    var text = document.getElementById("report-text");
    var stats = document.getElementById("report-stats");
    
    text.innerHTML = "";
    stats.innerHTML = "";
    
    rsp[1].report.forEach((part)=>{
        text.innerHTML += `${part.text}<br>`
        stats.innerHTML += `${part.amount} (${part.ratio}%)<br>`
    });
}

function logout() {
    localStorage.removeItem("password")
    open_page("login")
}

function search_student(value) {
    var studentTables = document.getElementById('studentTables')
    var children = studentTables.childNodes
    for (var i = 1;i<children.length;i++) {
        target = children[i]
        
        if (!(target.innerHTML.includes(value))) {
            target.style.display = "none";
        } 
    }
}

//document.getElementById("searchStudents").addEventListener("keypress", (ev)=>{
//    let value = ev.target.value+String.fromCharCode(ev.keyCode);
//    search_student(value);
//})