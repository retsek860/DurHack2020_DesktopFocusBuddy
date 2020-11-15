document.getElementById('pepehands').onclick = getExe();
//h.addEventListener('click', getExe());
function getExe() {
    let a = document.createElement('a')
    a.href = 'Steppe.exe'
    a.download = a.href.split('/').pop()
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
}
