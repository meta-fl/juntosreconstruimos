'use client';
import { useState, useEffect } from 'react';

export default function Home() {
  const [data, setData] = useState([]);
  const [tab, setTab] = useState('0');

  useEffect(() => {
    fetch('/api/iniciativas').then(res => res.json()).then(d => setData(d));
  }, []);

  const [form, setForm] = useState({ necesidad: '', linea: 'Salud y salud mental', urgencia: 'Media', quien_atiende: '', brecha: '', aporte: '', fase: 'Diagnóstico' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/api/iniciativas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    if (res.ok) {
      const newData = await res.json();
      setData(newData);
      setForm({ necesidad: '', linea: 'Salud y salud mental', urgencia: 'Media', quien_atiende: '', brecha: '', aporte: '', fase: 'Diagnóstico' });
    }
  };

  return (
    <>
      <div className="topbar">
        <div className="row">
          <div className="brand"><span className="dot"></span>Juntos Reconstruimos</div>
          <nav className="nav">
            <a href="#" onClick={() => setTab('0')} className={tab==='0'?'active':''}>FunLuker en acción</a>
            <a href="#" onClick={() => setTab('1')} className={tab==='1'?'active':''}>Teoría de cambio</a>
            <a href="#" onClick={() => setTab('2')} className={tab==='2'?'active':''}>Diagnóstico</a>
            <a href="#" onClick={() => setTab('3')} className={tab==='3'?'active':''}>Iniciativa</a>
            <a href="#" onClick={() => setTab('4')} className={tab==='4'?'active':''}>Matriz MEL</a>
          </nav>
        </div>
      </div>

      <section className="hero">
        <div className="wrap">
          <div className="eyebrow"><span className="ln"></span>Fundación Luker · Manizales y Caldas</div>
          <h1 className="title">Juntos reconstruimos</h1>
          <p className="sub">Un mismo lugar para levantar el diagnóstico, decidir qué ayuda se da y hacer seguimiento a lo que ese aporte deja instalado en el territorio.</p>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          {tab === '0' && (
            <div>
              <div className="sec-h"><h2>FunLuker en acción</h2></div>
              <div style={{backgroundColor: '#FFFCF6', border: '1px solid #DCD3C2', borderRadius: '12px', padding: '24px', marginBottom: '30px', boxShadow: '0 4px 12px rgba(64,42,28,0.04)'}}>
                <p style={{fontSize: '18px', color: '#402A1C', fontWeight: 500, fontStyle: 'italic', margin: 0}}>
                  "Este escenario exige actuar con solidaridad, pero también con prudencia. La Fundación Luker no debe partir de una oferta predeterminada de recursos sino de una comprensión rigurosa de las necesidades y de la respuesta que ya están adelantando las autoridades, las entidades de socorro y otras organizaciones. <strong style={{color:'#2B1B11'}}>El propósito inicial será, por tanto, entender antes de comprometer.</strong>"
                </p>
              </div>
              <h3 style={{color:'#2B1B11', marginTop:'10px', fontSize:'24px'}}>2. Objetivo del plan</h3>
              <p style={{marginTop:'15px', color:'#2B1B11'}}><strong>Contribuir a la atención y posterior recuperación de Manizales y Caldas</strong> frente a las afectaciones ocasionadas por el sismo, mediante una respuesta focalizada, ágil y complementaria...</p>
              
              <h3 style={{color:'#2B1B11', marginTop:'35px', marginBottom:'5px', fontSize:'24px'}}>3. Principios para la actuación</h3>
              <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px', marginTop:'20px'}}>
                <div style={{backgroundColor: '#FFFCF6', border: '1px solid #DCD3C2', borderRadius: '8px', padding: '20px', borderTop: '4px solid #8B5A2B'}}>
                  <div style={{color: '#8B5A2B', fontWeight: 'bold', fontFamily: 'monospace', fontSize: '11px', marginBottom: '8px'}}>PRINCIPIO 01</div>
                  <strong style={{color: '#402A1C', fontSize: '16px'}}>Información antes que intervención</strong>
                </div>
                <div style={{backgroundColor: '#FFFCF6', border: '1px solid #DCD3C2', borderRadius: '8px', padding: '20px', borderTop: '4px solid #46613F'}}>
                  <div style={{color: '#46613F', fontWeight: 'bold', fontFamily: 'monospace', fontSize: '11px', marginBottom: '8px'}}>PRINCIPIO 02</div>
                  <strong style={{color: '#402A1C', fontSize: '16px'}}>Complementariedad</strong>
                </div>
              </div>
            </div>
          )}

          {tab === '1' && (
            <div>
              <div className="sec-h"><h2>Teoría de Cambio</h2></div>
              <p>Aquí va el detalle de los supuestos e insumos...</p>
            </div>
          )}

          {tab === '2' && (
            <div>
              <div className="sec-h">
                <h2><span className="num">02</span>Fase de Diagnóstico</h2>
              </div>
              <p className="sec-note">Identificación de necesidades y evaluación de acceso y alcance actual.</p>
              
              <form className="add-form" onSubmit={handleSubmit}>
                <div className="grid-form">
                  <div>
                    <label>Necesidad identificada *</label>
                    <input type="text" value={form.necesidad} onChange={e=>setForm({...form, necesidad:e.target.value})} required/>
                  </div>
                  <div>
                    <label>Línea de Acción</label>
                    <select value={form.linea} onChange={e=>setForm({...form, linea:e.target.value})}>
                      <option>Equipo y aliados</option>
                      <option>Ayuda humanitaria</option>
                      <option>Salud y salud mental</option>
                      <option>Legado e instituciones religiosas</option>
                      <option>Reconstrucción educativa</option>
                    </select>
                  </div>
                  <div>
                    <label>Urgencia</label>
                    <select value={form.urgencia} onChange={e=>setForm({...form, urgencia:e.target.value})}>
                      <option>Alta</option><option>Media</option><option>Baja</option>
                    </select>
                  </div>
                  <div>
                    <label>¿Quién la está atendiendo?</label>
                    <input type="text" value={form.quien_atiende} onChange={e=>setForm({...form, quien_atiende:e.target.value})} />
                  </div>
                </div>
                <button type="submit" className="save-btn">Guardar Diagnóstico</button>
              </form>

              <div className="ptable-wrap">
                <table className="ptable">
                  <thead><tr>
                    <th>Necesidad identificada</th><th>Línea</th><th>Urgencia</th><th>¿Quién la atiende?</th>
                  </tr></thead>
                  <tbody>
                    {data.map((r, i) => (
                      <tr key={i}>
                        <td><strong>{r.necesidad}</strong></td>
                        <td>{r.linea}</td>
                        <td><span className={	ag }>{r.urgencia}</span></td>
                        <td>{r.quien_atiende}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {tab === '3' && <div><div className="sec-h"><h2>Iniciativa (Por definir)</h2></div></div>}
          {tab === '4' && <div><div className="sec-h"><h2>Matriz MEL (Por definir)</h2></div></div>}
        </div>
      </section>
    </>
  )
}
