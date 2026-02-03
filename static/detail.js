async function loadDetail() {
  const id = window.location.pathname.split('/').pop();
  const res = await fetch(`/users/${id}`);
  if (res.status !== 200) {
    document.getElementById('details').textContent = '未找到用户';
    return;
  }
  const u = await res.json();
  const container = document.getElementById('details');
  container.innerHTML = `
    <form id="editForm">
      <div class="mb-2">
        <label class="form-label">姓名</label>
        <input id="name" class="form-control" required value="${u.name}">
      </div>
      <div class="mb-2">
        <label class="form-label">邮箱</label>
        <input id="email" class="form-control" type="email" required value="${u.email}">
      </div>
      <div class="d-flex">
        <button class="btn btn-primary me-2" type="submit">保存</button>
        <button id="deleteBtn" class="btn btn-outline-danger" type="button">删除</button>
      </div>
      <div id="msg" class="mt-2 text-danger"></div>
    </form>
  `;

  document.getElementById('editForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const msg = document.getElementById('msg');
    msg.textContent = '';
    if (!name || !email) { msg.textContent = '请填写所有字段'; return; }
    const res = await fetch(`/users/${id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, email })
    });
    if (res.status === 200) {
      msg.className = 'mt-2 text-success';
      msg.textContent = '保存成功';
    } else {
      const j = await res.json().catch(()=>({error:'错误'}));
      msg.className = 'mt-2 text-danger';
      msg.textContent = j.error || '错误';
    }
  });

  document.getElementById('deleteBtn').addEventListener('click', async () => {
    if (!confirm('确定删除？')) return;
    await fetch(`/users/${id}`, { method: 'DELETE' });
    window.location.href = '/ui';
  });
}

window.addEventListener('load', loadDetail);
