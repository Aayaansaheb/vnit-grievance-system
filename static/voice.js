(function(){
  const btn = document.getElementById('start-voice');
  if(!btn) return;
  const ta = document.querySelector('textarea[name="description"]');
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ btn.disabled = true; btn.textContent = 'Voice not supported'; return; }
  const rec = new SR();
  rec.lang = 'en-IN';
  rec.continuous = false;
  rec.interimResults = false;
  btn.addEventListener('click', ()=>{ rec.start(); btn.textContent='Listening...'; });
  rec.onresult = (e)=>{
    const text = Array.from(e.results).map(r=>r[0].transcript).join(' ');
    ta.value = (ta.value? ta.value+"\n" : "") + text;
    btn.textContent='🎤 Voice (Emergency)';
  };
  rec.onerror = ()=>{ btn.textContent='🎤 Voice (Emergency)'; };
  rec.onend = ()=>{ btn.textContent='🎤 Voice (Emergency)'; };
})();
