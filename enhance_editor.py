from pathlib import Path
p = Path(r'D:\Projects\market-hours-beijing-timeline\index.html')
html = p.read_text(encoding='utf-8')

html = html.replace(
"""          <div class=\"control-box\">\n            <div class=\"control-label\">季节模式切换</div>\n            <div class=\"segmented\" id=\"seasonModeSwitch\">\n              <button data-mode=\"auto\" class=\"active\">自动</button>\n              <button data-mode=\"dst\">全夏令时</button>\n              <button data-mode=\"standard\">全冬令时</button>\n            </div>\n          </div>""",
"""          <div class=\"control-box\">\n            <div class=\"control-label\">季节模式切换</div>\n            <div class=\"segmented\" id=\"seasonModeSwitch\">\n              <button data-mode=\"auto\" class=\"active\">自动</button>\n              <button data-mode=\"dst\">全夏令时</button>\n              <button data-mode=\"standard\">全冬令时</button>\n            </div>\n          </div>\n          <div class=\"control-box\">\n            <div class=\"control-label\">编辑功能</div>\n            <div class=\"segmented\">\n              <button id=\"toggleEditorBtn\">编辑表格</button>\n              <button id=\"exportConfigBtn\">导出配置</button>\n            </div>\n          </div>""")

html = html.replace(
"""    </section>\n\n    <section class=\"desktop-view\">""",
"""    </section>\n\n    <section class=\"editor-panel\" id=\"editorPanel\" hidden>\n      <div class=\"view-title\">编辑模式（可新增市场 / 调整轨道 / 编辑文字与颜色）</div>\n      <div class=\"editor-wrap\">\n        <div class=\"editor-toolbar\">\n          <button id=\"addMarketBtn\">新增股市</button>\n          <button id=\"saveEditorBtn\">保存编辑</button>\n          <button id=\"resetEditorBtn\">恢复默认</button>\n          <span class=\"editor-tip\">桌面端可直接拖动柱状块移动，拖左右边缘调时长；双击柱状块可编辑文字和颜色。</span>\n        </div>\n        <div class=\"editor-layout\">\n          <div class=\"editor-list\" id=\"editorMarketList\"></div>\n          <div class=\"editor-form\" id=\"editorForm\">\n            <div class=\"editor-empty\">左侧选一个市场开始编辑</div>\n          </div>\n        </div>\n      </div>\n    </section>\n\n    <section class=\"desktop-view\">""")

css_insert = """
    .editor-panel{display:none;margin-top:14px;background:var(--panel);border:1px solid var(--line);border-radius:20px;box-shadow:0 16px 36px rgba(0,0,0,.22);backdrop-filter:blur(10px)}
    .editor-panel.show{display:block}
    .editor-wrap{padding:12px}
    .editor-toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
    .editor-toolbar button,.editor-form button,.editor-list button{border:1px solid var(--line-strong);background:rgba(255,255,255,.05);color:var(--text);padding:8px 12px;border-radius:10px;cursor:pointer}
    .editor-tip{font-size:12px;color:var(--muted)}
    .editor-layout{display:grid;grid-template-columns:280px 1fr;gap:12px}
    .editor-list,.editor-form{background:rgba(255,255,255,.035);border:1px solid var(--line);border-radius:14px;padding:12px}
    .editor-market-item{padding:10px 12px;border:1px solid var(--line);border-radius:10px;margin-bottom:8px;cursor:pointer;background:rgba(255,255,255,.03)}
    .editor-market-item.active{background:rgba(73,215,255,.16);border-color:rgba(73,215,255,.4)}
    .editor-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .editor-field{display:flex;flex-direction:column;gap:6px}
    .editor-field label{font-size:12px;color:var(--muted)}
    .editor-field input,.editor-field select,.editor-field textarea{width:100%;background:rgba(0,0,0,.18);color:var(--text);border:1px solid var(--line);border-radius:10px;padding:8px 10px}
    .editor-field textarea{min-height:72px;resize:vertical}
    .segment-list{margin-top:12px;display:flex;flex-direction:column;gap:8px}
    .segment-item{border:1px solid var(--line);border-radius:12px;padding:10px;background:rgba(255,255,255,.03)}
    .segment-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:8px}
    .track.editable-track,.mobile-market-track.editable-track{outline:1px dashed rgba(73,215,255,.28)}
    .segment.editable,.mobile-segment.editable{cursor:move}
    .segment-handle{position:absolute;top:0;bottom:0;width:8px;z-index:5}
    .segment-handle.left{left:0;cursor:ew-resize}
    .segment-handle.right{right:0;cursor:ew-resize}
    .mobile-editor-actions{display:none}
    @media (max-width:980px){
      .editor-layout{grid-template-columns:1fr}
      .mobile-editor-actions{display:flex;gap:6px;justify-content:center;position:sticky;bottom:8px;z-index:30;margin-top:8px}
    }
"""
html = html.replace("""    @keyframes linePulse{\n      0%{opacity:.55;filter:brightness(.9)}\n      50%{opacity:1;filter:brightness(1.25)}\n      100%{opacity:.55;filter:brightness(.9)}\n    }\n""", css_insert + "\n    @keyframes linePulse{\n      0%{opacity:.55;filter:brightness(.9)}\n      50%{opacity:1;filter:brightness(1.25)}\n      100%{opacity:.55;filter:brightness(.9)}\n    }\n")

js_old = """    const state = { seasonMode: 'auto' };\n    const weekdayMap = ['周日','周一','周二','周三','周四','周五','周六'];\n"""
js_new = """    const defaultMarkets = JSON.parse(JSON.stringify(markets));\n    const STORAGE_KEY = 'marketTimelineCustomMarketsV1';\n    function loadCustomMarkets(){\n      try{\n        const raw = localStorage.getItem(STORAGE_KEY);\n        if(!raw) return null;\n        const parsed = JSON.parse(raw);\n        return Array.isArray(parsed) ? parsed : null;\n      }catch(e){ return null; }\n    }\n    const customMarkets = loadCustomMarkets();\n    if(customMarkets) {\n      markets.length = 0;\n      customMarkets.forEach(m => markets.push(m));\n    }\n\n    const state = { seasonMode: 'auto', editorOpen:false, selectedMarketKey:null, drag:null };\n    const weekdayMap = ['周日','周一','周二','周三','周四','周五','周六'];\n"""
html = html.replace(js_old, js_new)

marker = """    bindSeasonSwitch();\n    render();\n    setInterval(render,1000);\n    window.addEventListener('resize', ()=>{ const now = new Date(); setDesktopLine(now); setMobileLine(now); });\n  </script>"""
insert = """
    function saveCustomMarkets(){
      localStorage.setItem(STORAGE_KEY, JSON.stringify(markets));
    }
    function exportConfig(){
      const text = JSON.stringify(markets, null, 2);
      navigator.clipboard?.writeText(text).catch(()=>{});
      alert('当前配置已复制到剪贴板');
    }
    function marketByKey(key){ return markets.find(m=>m.key===key); }
    function ensureSessions(market){
      market.sessions = market.sessions || { standard: [], dst: [] };
      market.sessions.standard = market.sessions.standard || [];
      market.sessions.dst = market.sessions.dst || [];
    }
    function normalizeLabel(market){
      const build = items => items.filter(x=>x.type!=='break' || true).map(x=>`${x.start}-${x.end}${x.type==='break'?'(休)': x.type==='dark'?'(暗)':''}`).join(' / ');
      market.standardLabel = build(market.sessions.standard);
      market.dstLabel = build(market.sessions.dst);
    }
    function addMarket(){
      const key = `m${Date.now().toString(36)}`;
      const m = { key, name:'新市场', zone:'Asia/Shanghai', standardLabel:'09:00-15:00', dstLabel:'09:00-15:00', sessions:{ standard:[{start:'09:00',end:'15:00',type:'open',label:'交易',color:'#49d7ff'}], dst:[{start:'09:00',end:'15:00',type:'open',label:'交易',color:'#49d7ff'}] } };
      markets.push(m);
      state.selectedMarketKey = key;
      saveCustomMarkets();
      render();
      renderEditor();
    }
    function deleteMarket(key){
      const idx = markets.findIndex(x=>x.key===key);
      if(idx>=0) markets.splice(idx,1);
      if(state.selectedMarketKey===key) state.selectedMarketKey = markets[0]?.key || null;
      saveCustomMarkets();
      render();
      renderEditor();
    }
    function addSegment(key, mode){
      const market = marketByKey(key); if(!market) return;
      ensureSessions(market);
      market.sessions[mode].push({start:'09:00',end:'10:00',type:'open',label:'新段',color:'#49d7ff'});
      normalizeLabel(market); saveCustomMarkets(); render(); renderEditor();
    }
    function updateMarketField(key, field, value){
      const market = marketByKey(key); if(!market) return;
      market[field] = value;
      saveCustomMarkets(); render(); renderEditor();
    }
    function updateSegment(key, mode, idx, field, value){
      const market = marketByKey(key); if(!market) return;
      ensureSessions(market);
      market.sessions[mode][idx][field] = value;
      normalizeLabel(market); saveCustomMarkets(); render(); renderEditor();
    }
    function removeSegment(key, mode, idx){
      const market = marketByKey(key); if(!market) return;
      market.sessions[mode].splice(idx,1);
      normalizeLabel(market); saveCustomMarkets(); render(); renderEditor();
    }
    function buildSegmentEditor(key, mode, seg, idx){
      return `<div class="segment-item">
        <div class="editor-grid">
          <div class="editor-field"><label>开始</label><input data-role="seg" data-key="${key}" data-mode="${mode}" data-idx="${idx}" data-field="start" value="${seg.start||''}"></div>
          <div class="editor-field"><label>结束</label><input data-role="seg" data-key="${key}" data-mode="${mode}" data-idx="${idx}" data-field="end" value="${seg.end||''}"></div>
          <div class="editor-field"><label>类型</label><select data-role="seg" data-key="${key}" data-mode="${mode}" data-idx="${idx}" data-field="type"><option value="open" ${seg.type==='open'?'selected':''}>交易</option><option value="break" ${seg.type==='break'?'selected':''}>午休</option><option value="dark" ${seg.type==='dark'?'selected':''}>暗盘/扩展</option></select></div>
          <div class="editor-field"><label>文字</label><input data-role="seg" data-key="${key}" data-mode="${mode}" data-idx="${idx}" data-field="label" value="${seg.label||''}"></div>
          <div class="editor-field"><label>颜色</label><input type="color" data-role="seg" data-key="${key}" data-mode="${mode}" data-idx="${idx}" data-field="color" value="${seg.color||'#49d7ff'}"></div>
        </div>
        <div class="segment-actions"><button data-action="remove-seg" data-key="${key}" data-mode="${mode}" data-idx="${idx}">删除柱</button></div>
      </div>`;
    }
    function renderEditor(){
      const panel = document.getElementById('editorPanel');
      panel.classList.toggle('show', state.editorOpen);
      panel.hidden = !state.editorOpen;
      const list = document.getElementById('editorMarketList');
      const form = document.getElementById('editorForm');
      list.innerHTML = markets.map(m=>`<div class="editor-market-item ${state.selectedMarketKey===m.key?'active':''}" data-action="pick-market" data-key="${m.key}"><strong>${m.name}</strong><div style="font-size:12px;color:var(--muted);margin-top:4px">${m.key}</div></div>`).join('') + '<button id="addMarketBtnInline">+ 新增股市</button>';
      const market = marketByKey(state.selectedMarketKey) || markets[0];
      if(market && !state.selectedMarketKey) state.selectedMarketKey = market.key;
      if(!market){ form.innerHTML = '<div class="editor-empty">还没有市场，先新增一个。</div>'; bindEditorEvents(); return; }
      ensureSessions(market);
      form.innerHTML = `
        <div class="editor-grid">
          <div class="editor-field"><label>市场名称</label><input id="marketNameInput" value="${market.name}"></div>
          <div class="editor-field"><label>时区</label><input id="marketZoneInput" value="${market.zone}"></div>
          <div class="editor-field"><label>冬令时标签</label><input id="marketStandardLabelInput" value="${market.standardLabel}"></div>
          <div class="editor-field"><label>夏令时标签</label><input id="marketDstLabelInput" value="${market.dstLabel}"></div>
        </div>
        <div class="segment-list">
          <h3>冬令时轨道</h3>
          ${(market.sessions.standard||[]).map((seg,idx)=>buildSegmentEditor(market.key,'standard',seg,idx)).join('')}
          <button data-action="add-seg" data-key="${market.key}" data-mode="standard">+ 添加冬令时柱状图</button>
          <h3 style="margin-top:14px">夏令时轨道</h3>
          ${(market.sessions.dst||[]).map((seg,idx)=>buildSegmentEditor(market.key,'dst',seg,idx)).join('')}
          <button data-action="add-seg" data-key="${market.key}" data-mode="dst">+ 添加夏令时柱状图</button>
          <div class="segment-actions" style="justify-content:space-between"><button data-action="delete-market" data-key="${market.key}">删除市场</button><button id="saveCurrentMarketBtn">应用当前市场修改</button></div>
        </div>
        <div class="mobile-editor-actions"><button id="mobileAddSegStandard">冬令时加柱</button><button id="mobileAddSegDst">夏令时加柱</button></div>
      `;
      bindEditorEvents();
    }
    function bindEditorEvents(){
      document.querySelectorAll('[data-action="pick-market"]').forEach(el=>el.onclick=()=>{ state.selectedMarketKey = el.dataset.key; renderEditor(); });
      document.querySelectorAll('[data-action="add-seg"]').forEach(el=>el.onclick=()=>addSegment(el.dataset.key, el.dataset.mode));
      document.querySelectorAll('[data-action="delete-market"]').forEach(el=>el.onclick=()=>deleteMarket(el.dataset.key));
      document.querySelectorAll('[data-action="remove-seg"]').forEach(el=>el.onclick=()=>removeSegment(el.dataset.key, el.dataset.mode, +el.dataset.idx));
      document.querySelectorAll('[data-role="seg"]').forEach(el=>el.onchange=()=>updateSegment(el.dataset.key, el.dataset.mode, +el.dataset.idx, el.dataset.field, el.value));
      const nameInput = document.getElementById('marketNameInput');
      const zoneInput = document.getElementById('marketZoneInput');
      const standardLabelInput = document.getElementById('marketStandardLabelInput');
      const dstLabelInput = document.getElementById('marketDstLabelInput');
      const market = marketByKey(state.selectedMarketKey);
      document.getElementById('saveCurrentMarketBtn')?.addEventListener('click', ()=>{
        if(!market) return;
        updateMarketField(market.key,'name',nameInput.value);
        updateMarketField(market.key,'zone',zoneInput.value);
        updateMarketField(market.key,'standardLabel',standardLabelInput.value);
        updateMarketField(market.key,'dstLabel',dstLabelInput.value);
      });
      document.getElementById('addMarketBtnInline')?.addEventListener('click', addMarket);
      document.getElementById('mobileAddSegStandard')?.addEventListener('click', ()=>addSegment(state.selectedMarketKey,'standard'));
      document.getElementById('mobileAddSegDst')?.addEventListener('click', ()=>addSegment(state.selectedMarketKey,'dst'));
    }
    function styleSegment(el, seg){
      if(seg.color){
        if(el.classList.contains('mobile-segment')) el.style.background = `linear-gradient(180deg, ${seg.color}, ${seg.color}cc)`;
        else el.style.background = `linear-gradient(90deg, ${seg.color}, ${seg.color}cc)`;
      }
    }
    function bindTrackEditor(){
      if(!state.editorOpen) return;
      document.querySelectorAll('.track .segment, .mobile-market-track .mobile-segment').forEach(segEl=>{
        segEl.classList.add('editable');
        if(segEl.querySelector('.segment-handle')) return;
        const left = document.createElement('i'); left.className = 'segment-handle left';
        const right = document.createElement('i'); right.className = 'segment-handle right';
        segEl.appendChild(left); segEl.appendChild(right);
      });
      document.querySelectorAll('.track').forEach(track=>track.classList.add('editable-track'));
      document.querySelectorAll('.mobile-market-track').forEach(track=>track.classList.add('editable-track'));
    }
    function minuteFromDesktopPointer(track, clientX){
      const rect = track.getBoundingClientRect();
      const ratio = Math.min(1, Math.max(0, (clientX - rect.left)/rect.width));
      return Math.round(ratio*1440);
    }
    function minuteFromMobilePointer(track, clientY){
      const rect = track.getBoundingClientRect();
      const ratio = Math.min(1, Math.max(0, (clientY - rect.top)/rect.height));
      return Math.round(ratio*1440);
    }
    function attachSegmentMeta(el, marketKey, mode, idx){
      el.dataset.marketKey = marketKey; el.dataset.mode = mode; el.dataset.idx = idx;
    }
    function promptEditSegment(marketKey, mode, idx){
      const market = marketByKey(marketKey); if(!market) return;
      const seg = market.sessions[mode][idx]; if(!seg) return;
      const label = prompt('编辑文字', seg.label || '');
      if(label !== null) seg.label = label;
      const color = prompt('输入颜色值（如 #49d7ff）', seg.color || '#49d7ff');
      if(color) seg.color = color;
      normalizeLabel(market); saveCustomMarkets(); render(); renderEditor();
    }
    function bindEditorGestureLayer(){
      document.addEventListener('dblclick', (e)=>{
        const seg = e.target.closest('.segment, .mobile-segment');
        if(!state.editorOpen || !seg) return;
        promptEditSegment(seg.dataset.marketKey, seg.dataset.mode, +seg.dataset.idx);
      });
      document.addEventListener('pointerdown', (e)=>{
        if(!state.editorOpen) return;
        const handle = e.target.closest('.segment-handle');
        const seg = e.target.closest('.segment, .mobile-segment');
        if(!seg) return;
        state.drag = { type: handle ? (handle.classList.contains('left') ? 'resize-left' : 'resize-right') : 'move', mobile: seg.classList.contains('mobile-segment'), marketKey: seg.dataset.marketKey, mode: seg.dataset.mode, idx: +seg.dataset.idx, track: seg.parentElement };
      });
      document.addEventListener('pointermove', (e)=>{
        if(!state.editorOpen || !state.drag) return;
        const market = marketByKey(state.drag.marketKey); if(!market) return;
        const seg = market.sessions[state.drag.mode][state.drag.idx]; if(!seg) return;
        const minute = state.drag.mobile ? minuteFromMobilePointer(state.drag.track, e.clientY) : minuteFromDesktopPointer(state.drag.track, e.clientX);
        const start = parseMinutes(seg.start), end = parseMinutes(seg.end), dur = Math.max(10, end-start);
        if(state.drag.type === 'move'){
          let newStart = Math.min(1430-dur, Math.max(0, minute - Math.round(dur/2)));
          seg.start = formatMinuteLabel(newStart); seg.end = formatMinuteLabel(newStart + dur);
        } else if(state.drag.type === 'resize-left'){
          const newStart = Math.min(end-10, Math.max(0, minute));
          seg.start = formatMinuteLabel(newStart);
        } else if(state.drag.type === 'resize-right'){
          const newEnd = Math.max(start+10, Math.min(1440, minute));
          seg.end = formatMinuteLabel(newEnd);
        }
        normalizeLabel(market); saveCustomMarkets(); render(); renderEditor();
      });
      document.addEventListener('pointerup', ()=>{ state.drag = null; });
    }
    const originalBuildDesktop = buildDesktop;
    buildDesktop = function(date){
      const sorted = [...markets].sort((a,b)=>getEarliestOpen(a,date)-getEarliestOpen(b,date));
      desktopGrid.innerHTML='';
      const axis = document.createElement('div');
      axis.className='axis-row';
      axis.innerHTML='<div class="axis-name">市场 / 北京时间</div><div class="axis-track" id="axisTrack"></div>';
      desktopGrid.appendChild(axis);
      const axisTrack = axis.querySelector('#axisTrack');
      for(let i=0;i<=24;i++){
        const h=document.createElement('div'); h.className=`hour ${i % 2 === 0 ? 'major' : 'minor'}`; h.style.left=`${(i/24)*100}%`; h.textContent=`${pad(i)}:00`; axisTrack.appendChild(h);
      }
      sorted.forEach(market=>{
        const status = marketStatus(market,date);
        const row=document.createElement('div');
        const shouldHighlight = !isWeekendBeijing(date) && isMarketActiveNow(market,date);
        row.className=`market-row ${shouldHighlight?'active':'dimmed'} ${isSaturdayBeijing(date)?'weekend':''}`;
        const leftInfo = status.closedByCalendar ? '休市' : (status.specialByCalendar ? '特殊时段' : (status.mode==='dst'?market.dstLabel:market.standardLabel));
        row.innerHTML=`<div class="market-meta"><div class="market-name">${market.name}</div><div class="market-info">${leftInfo}</div></div><div class="track"></div>`;
        const track = row.querySelector('.track');
        const mode = resolvedMode(market,date);
        const items = (market.sessions[mode] || []);
        const breakActive = !!status.onBreak;
        items.forEach((seg,idx)=>{
          const s=parseMinutes(seg.start), e=parseMinutes(seg.end); const duration = e - s;
          const el=document.createElement('div'); el.className=`segment ${seg.type}`; el.style.top='7px'; el.style.height='14px'; el.style.left=`${minutePercent(s)}%`; el.style.width=`${minutePercent(duration)}%`;
          el.textContent = duration <= 45 ? `${seg.start}` : duration <= 90 ? `${seg.start}-${seg.end}` : `${seg.label||''} ${seg.start}-${seg.end}`.trim();
          const isCurrentSeg = status.minute>=s && status.minute<e;
          if(seg.type === 'break') { if(isCurrentSeg) el.classList.add('is-active'); else el.classList.add('is-inactive-break'); } else { if(isCurrentSeg && !breakActive) el.classList.add('is-active'); if(breakActive) el.classList.add('is-muted-by-break'); }
          styleSegment(el, seg); attachSegmentMeta(el, market.key, mode, idx); track.appendChild(el);
        });
        desktopGrid.appendChild(row);
      });
      desktopCurrentLine.style.left=`calc(var(--name-w) + ${minutePercent(currentBeijingMinute(date))}% * (100% - var(--name-w)) / 100)`;
      bindTrackEditor();
    }
    const originalBuildMobile = buildMobile;
    buildMobile = function(date){
      const single = document.getElementById('mobileSingle');
      const prevScrollLeft = single ? single.scrollLeft : 0;
      mobileGrid.innerHTML='';
      const sorted=[...markets].sort((a,b)=>getEarliestOpen(a,date)-getEarliestOpen(b,date));
      const axisCol = document.createElement('div'); axisCol.className='mobile-axis-col'; axisCol.innerHTML='<div class="mobile-axis-title">时间</div><div class="mobile-axis-track" id="mobileAxisTrack"></div>';
      const axisHeight = getMobileAxisHeight(); const axisTotalHeight = axisHeight + MOBILE_BOTTOM_SAFE_PX; axisCol.style.height = `${axisTotalHeight}px`; mobileGrid.appendChild(axisCol);
      const axisTrack = axisCol.querySelector('#mobileAxisTrack'); axisTrack.style.height = `${axisHeight - MOBILE_HEADER_OFFSET}px`;
      for(let i=0;i<=24;i++){ const h=document.createElement('div'); h.className=`mobile-hour ${i % 2 === 0 ? 'major' : 'minor'}`; h.style.top=`${(i/24)*100}%`; h.textContent=`${pad(i)}:00`; axisTrack.appendChild(h); }
      sorted.forEach(market=>{
        const status = marketStatus(market,date); const col = document.createElement('div'); const shouldHighlight = !isWeekendBeijing(date) && isMarketActiveNow(market,date);
        col.className=`mobile-market-col ${shouldHighlight?'active':'dimmed'} ${isSaturdayBeijing(date)?'weekend':''}`; col.dataset.marketKey = market.key;
        const mobileInfo = status.closedByCalendar ? '休市' : (status.specialByCalendar ? '特殊时段' : (status.mode==='dst'?market.dstLabel:market.standardLabel));
        col.innerHTML=`<div class="mobile-market-head"><div class="mobile-market-name">${market.name}</div><div class="mobile-market-info">${mobileInfo}</div></div><div class="mobile-market-track"></div>`;
        col.style.height = `${axisTotalHeight}px`; col.style.minWidth = '28px';
        const track = col.querySelector('.mobile-market-track'); const mode = resolvedMode(market,date); const items = (market.sessions[mode] || []); const breakActive = !!status.onBreak;
        items.forEach((seg,idx)=>{ const s=parseMinutes(seg.start), e=parseMinutes(seg.end); const duration = e - s; const el=document.createElement('div'); el.className=`mobile-segment segment ${seg.type}`; el.style.top=`${minutePercent(s)}%`; el.style.height=`${minutePercent(duration)}%`; el.innerHTML = `<span class="v">${compactMobileLabel(seg.label || (seg.type === 'break' ? '午休' : '交易'))}</span>`; const isCurrentSeg = status.minute>=s && status.minute<e; if(seg.type === 'break') { if(isCurrentSeg) el.classList.add('is-active'); else el.classList.add('is-inactive-break'); } else { if(isCurrentSeg && !breakActive) el.classList.add('is-active'); if(breakActive) el.classList.add('is-muted-by-break'); } styleSegment(el, seg); attachSegmentMeta(el, market.key, mode, idx); track.appendChild(el); });
        mobileGrid.appendChild(col);
      });
      setMobileLine(date); if (single) single.scrollLeft = prevScrollLeft; bindTrackEditor();
    }
    function bindEditorUI(){
      document.getElementById('toggleEditorBtn')?.addEventListener('click', ()=>{ state.editorOpen = !state.editorOpen; if(!state.selectedMarketKey) state.selectedMarketKey = markets[0]?.key || null; renderEditor(); render(); });
      document.getElementById('exportConfigBtn')?.addEventListener('click', exportConfig);
      document.getElementById('addMarketBtn')?.addEventListener('click', addMarket);
      document.getElementById('saveEditorBtn')?.addEventListener('click', ()=>{ saveCustomMarkets(); alert('编辑已保存到本地浏览器'); });
      document.getElementById('resetEditorBtn')?.addEventListener('click', ()=>{ if(!confirm('确定恢复默认市场配置？')) return; localStorage.removeItem(STORAGE_KEY); markets.length=0; defaultMarkets.forEach(m=>markets.push(JSON.parse(JSON.stringify(m)))); state.selectedMarketKey = markets[0]?.key || null; render(); renderEditor(); });
    }
    bindSeasonSwitch();
    bindEditorUI();
    bindEditorGestureLayer();
    render();
    setInterval(render,1000);
    window.addEventListener('resize', ()=>{ const now = new Date(); setDesktopLine(now); setMobileLine(now); });
  </script>"""
html = html.replace(marker, insert)

p.write_text(html, encoding='utf-8')
print('ok')
