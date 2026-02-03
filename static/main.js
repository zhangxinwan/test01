async function listUsers() {
  const res = await fetch('/users');
  const users = await res.json();
  const list = document.getElementById('usersList');
  list.innerHTML = '';
  users.forEach(u => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.innerHTML = `<div><strong>${u.name}</strong><br><small>${u.email}</small></div>`;
    const btns = document.createElement('div');

    const del = document.createElement('button');
    del.className = 'btn btn-sm btn-outline-danger ms-2';
    del.textContent = '删除';
    del.onclick = async () => {
      if (!confirm('确定删除？')) return;
      await fetch(`/users/${u.id}`, { method: 'DELETE' });
      listUsers();
    };

    btns.appendChild(del);
    li.appendChild(btns);
    list.appendChild(li);
  });
}

document.getElementById('createForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('nameInput').value.trim();
  const email = document.getElementById('emailInput').value.trim();
  const msg = document.getElementById('createMessage');
  msg.textContent = '';
  const res = await fetch('/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email }),
  });
  if (res.status === 201) {
    document.getElementById('createForm').reset();
    listUsers();
  } else {
    const j = await res.json().catch(()=>({error:'请求失败'}));
    msg.textContent = j.error || '错误';
  }
});

window.addEventListener('load', () => {
  listUsers();
});
