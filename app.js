const authMsg = document.getElementById('authMsg');
const registerBtn = document.getElementById('registerBtn');
const loginBtn = document.getElementById('loginBtn');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const appDiv = document.getElementById('app');
const authDiv = document.getElementById('auth');
const notesList = document.getElementById('notesList');
const createNoteBtn = document.getElementById('createNoteBtn');
const noteTitle = document.getElementById('noteTitle');
const noteContent = document.getElementById('noteContent');
const logoutBtn = document.getElementById('logoutBtn');

function setToken(token){
    localStorage.setItem('auth_token', token);
}
function getToken(){
    return localStorage.getItem('auth_token');
}
function showApp(){
    authDiv.style.display = 'none';
    appDiv.style.display = 'block';
    loadNotes();
}
function showAuth(msg=''){
    authDiv.style.display = 'block';
    appDiv.style.display = 'none';
    authMsg.innerText = msg;
}

async function api(path, method='GET', body=null){
    const headers = {'Content-Type':'application/json'};
    const token = getToken();
    if(token) headers['Authorization'] = 'Bearer ' + token;
    const res = await fetch(path, {method, headers, body: body? JSON.stringify(body): undefined});
    return res;
}

registerBtn.onclick = async ()=>{
    const res = await api('/auth/register','POST',{username: usernameInput.value, password: passwordInput.value});
    const data = await res.json();
    if(res.ok){
        setToken(data.access_token);
        showApp();
    } else {
        showAuth(data.msg || 'Error registering');
    }
};

loginBtn.onclick = async ()=>{
    const res = await api('/auth/login','POST',{username: usernameInput.value, password: passwordInput.value});
    const data = await res.json();
    if(res.ok){
        setToken(data.access_token);
        showApp();
    } else {
        showAuth(data.msg || 'Error logging in');
    }
};

createNoteBtn.onclick = async ()=>{
    const res = await api('/api/notes','POST',{title: noteTitle.value, content: noteContent.value});
    if(res.ok){
        noteTitle.value=''; noteContent.value='';
        loadNotes();
    } else {
        alert('Could not create note');
    }
};

async function loadNotes(){
    const res = await api('/api/notes','GET');
    if(res.ok){
        const notes = await res.json();
        notesList.innerHTML = '';
        for(const n of notes){
            const li = document.createElement('li');
            li.innerHTML = `<strong>${n.title}</strong> - ${n.content || ''} <button data-id="${n.id}" class="del">Delete</button>`;
            notesList.appendChild(li);
        }
        document.querySelectorAll('.del').forEach(b=> b.onclick = async ()=>{
            const id = b.getAttribute('data-id');
            const r = await api('/api/notes/'+id,'DELETE');
            if(r.ok) loadNotes();
        });
    } else {
        // token invalid or not logged in
        showAuth('Please login again.');
    }
}

logoutBtn.onclick = ()=>{
    localStorage.removeItem('auth_token');
    showAuth('Logged out.');
}

// on load, check if token present
if(getToken()) showApp(); else showAuth();
