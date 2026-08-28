<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
  
  :root {
    --spice-gold: #D4A574;
    --deep-orange: #C2622D;
    --dark-brown: #3D2312;
    --arrakis-black: #0A0A0A;
    --fremen-blue: #00B4D8;
    --sand-light: #E8DCC4;
    --shadow-deep: rgba(0, 0, 0, 0.8);
  }
  
  * {
    box-sizing: border-box;
  }
  
  body {
    background: var(--arrakis-black);
    color: var(--sand-light);
    font-family: 'Space Mono', monospace;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
  }
  
  .dune-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
  }
  
  /* Sand Particles Animation */
  .sand-particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
  }
  
  .particle {
    position: absolute;
    width: 3px;
    height: 3px;
    background: var(--spice-gold);
    border-radius: 50%;
    opacity: 0;
    animation: float 8s infinite ease-in-out;
  }
  
  @keyframes float {
    0% {
      opacity: 0;
      transform: translateY(100vh) translateX(0);
    }
    10% {
      opacity: 0.8;
    }
    90% {
      opacity: 0.3;
    }
    100% {
      opacity: 0;
      transform: translateY(-10vh) translateX(100px);
    }
  }
  
  /* Cinematic Header */
  .cinematic-header {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, var(--arrakis-black) 0%, var(--dark-brown) 50%, var(--arrakis-black) 100%);
    border: 2px solid var(--spice-gold);
    border-radius: 10px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    animation: fadeInBlur 2s ease-out forwards;
    opacity: 0;
  }
  
  .cinematic-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(212, 165, 116, 0.1) 0%, transparent 70%);
    animation: spiceGlow 4s ease-in-out infinite;
  }
  
  @keyframes spiceGlow {
    0%, 100% { transform: scale(1) rotate(0deg); }
    50% { transform: scale(1.1) rotate(180deg); }
  }
  
  @keyframes fadeInBlur {
    0% {
      opacity: 0;
      filter: blur(10px);
      transform: translateY(30px);
    }
    100% {
      opacity: 1;
      filter: blur(0);
      transform: translateY(0);
    }
  }
  
  .name-title {
    font-family: 'Cinzel', serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: var(--spice-gold);
    text-shadow: 0 0 30px rgba(212, 165, 116, 0.5);
    margin: 0;
    animation: titleReveal 1.5s ease-out 0.5s forwards;
    opacity: 0;
  }
  
  @keyframes titleReveal {
    0% {
      opacity: 0;
      letter-spacing: 20px;
    }
    100% {
      opacity: 1;
      letter-spacing: 5px;
    }
  }
  
  .spice-quote {
    font-style: italic;
    color: var(--deep-orange);
    margin-top: 20px;
    font-size: 0.9rem;
    animation: fadeIn 1s ease-out 1.5s forwards;
    opacity: 0;
  }
  
  @keyframes fadeIn {
    to { opacity: 1; }
  }
  
  /* Stats Section - Spice Harvest Data */
  .spice-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 40px 0;
  }
  
  .stat-card {
    background: linear-gradient(145deg, var(--dark-brown), var(--arrakis-black));
    border: 1px solid var(--spice-gold);
    border-radius: 10px;
    padding: 25px;
    text-align: center;
    transition: all 0.4s ease;
    animation: slideUp 0.8s ease-out forwards;
    opacity: 0;
    transform: translateY(30px);
  }
  
  .stat-card:nth-child(1) { animation-delay: 0.2s; }
  .stat-card:nth-child(2) { animation-delay: 0.4s; }
  .stat-card:nth-child(3) { animation-delay: 0.6s; }
  .stat-card:nth-child(4) { animation-delay: 0.8s; }
  
  @keyframes slideUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .stat-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 10px 40px rgba(212, 165, 116, 0.3);
    border-color: var(--fremen-blue);
  }
  
  .stat-icon {
    font-size: 2.5rem;
    margin-bottom: 10px;
  }
  
  .stat-label {
    color: var(--spice-gold);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  
  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--sand-light);
    margin-top: 5px;
  }
  
  /* GitHub Stats Section */
  .github-stats {
    background: linear-gradient(135deg, var(--arrakis-black), var(--dark-brown));
    border: 2px solid var(--deep-orange);
    border-radius: 15px;
    padding: 30px;
    margin: 40px 0;
    text-align: center;
  }
  
  .github-stats img {
    margin: 10px;
    border-radius: 8px;
  }
  
  .stats-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }
  
  /* Tech Still Suit */
  .still-suit {
    background: var(--dark-brown);
    border: 2px solid var(--deep-orange);
    border-radius: 15px;
    padding: 30px;
    margin: 40px 0;
    position: relative;
    overflow: hidden;
  }
  
  .still-suit::after {
    content: 'FREMEN SURVIVAL GEAR';
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 0.7rem;
    color: var(--deep-orange);
    letter-spacing: 3px;
    opacity: 0.7;
  }
  
  .section-title {
    font-family: 'Cinzel', serif;
    font-size: 1.8rem;
    color: var(--spice-gold);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 15px;
  }
  
  .tech-item {
    background: var(--arrakis-black);
    border: 1px solid var(--spice-gold);
    border-radius: 8px;
    padding: 15px 10px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
  }
  
  .tech-item:hover {
    background: var(--spice-gold);
    color: var(--arrakis-black);
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(212, 165, 116, 0.5);
  }
  
  .tech-item img {
    width: 40px;
    height: 40px;
    margin-bottom: 8px;
  }
  
  .tech-item span {
    display: block;
    font-size: 0.75rem;
    margin-top: 5px;
  }
  
  /* Projects - Sietches */
  .sietches {
    margin: 40px 0;
  }
  
  .sietch-card {
    background: linear-gradient(135deg, var(--arrakis-black), var(--dark-brown));
    border: 1px solid var(--spice-gold);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 20px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 20px;
    align-items: center;
    transition: all 0.4s ease;
    animation: fadeInLeft 0.6s ease-out forwards;
    opacity: 0;
    transform: translateX(-30px);
  }
  
  .sietch-card:nth-child(odd) { animation-delay: 0.3s; }
  .sietch-card:nth-child(even) { animation-delay: 0.5s; }
  
  @keyframes fadeInLeft {
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  .sietch-card:hover {
    border-color: var(--fremen-blue);
    box-shadow: 0 5px 30px rgba(0, 180, 216, 0.2);
    transform: translateX(10px);
  }
  
  .sietch-info h3 {
    font-family: 'Cinzel', serif;
    color: var(--spice-gold);
    font-size: 1.3rem;
    margin-bottom: 8px;
  }
  
  .sietch-info p {
    color: var(--sand-light);
    font-size: 0.9rem;
    opacity: 0.8;
  }
  
  .sietch-links {
    display: flex;
    gap: 10px;
  }
  
  .sietch-link {
    background: var(--deep-orange);
    color: var(--arrakis-black);
    padding: 8px 15px;
    border-radius: 5px;
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 700;
    transition: all 0.3s ease;
  }
  
  .sietch-link:hover {
    background: var(--fremen-blue);
    transform: scale(1.05);
  }
  
  /* Worm Path - Activity */
  .worm-path {
    background: var(--dark-brown);
    border: 2px solid var(--deep-orange);
    border-radius: 15px;
    padding: 25px;
    margin: 40px 0;
    text-align: center;
  }
  
  .worm-path img {
    border-radius: 10px;
    max-width: 100%;
  }
  
  /* Snake Animation */
  .snake-container {
    margin: 30px 0;
    text-align: center;
  }
  
  .snake-container img {
    border-radius: 10px;
    max-width: 100%;
  }
  
  /* Fremen Network */
  .fremen-network {
    background: linear-gradient(135deg, var(--arrakis-black), var(--dark-brown));
    border: 2px solid var(--fremen-blue);
    border-radius: 15px;
    padding: 30px;
    margin: 40px 0;
    text-align: center;
  }
  
  .collab-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
  }
  
  .collab-item {
    background: var(--arrakis-black);
    border: 1px solid var(--spice-gold);
    border-radius: 20px;
    padding: 10px 20px;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }
  
  .collab-item:hover {
    background: var(--spice-gold);
    color: var(--arrakis-black);
    transform: translateY(-3px);
  }
  
  /* Footer */
  .dune-footer {
    text-align: center;
    padding: 40px 20px;
    border-top: 1px solid var(--spice-gold);
    margin-top: 60px;
  }
  
  .blessing {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    color: var(--deep-orange);
    font-style: italic;
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 1; text-shadow: 0 0 20px rgba(194, 98, 45, 0.5); }
  }
  
  .social-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }
  
  .social-link {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    border: 2px solid var(--spice-gold);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-size: 1.3rem;
    transition: all 0.3s ease;
  }
  
  .social-link:hover {
    background: var(--spice-gold);
    color: var(--arrakis-black);
    transform: rotate(360deg) scale(1.2);
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .name-title {
      font-size: 2rem;
    }
    
    .sietch-card {
      grid-template-columns: 1fr;
    }
    
    .sietch-links {
      justify-content: flex-start;
    }
    
    .stats-row {
      flex-direction: column;
      align-items: center;
    }
  }
</style>

<!-- Sand Particles -->
<div class="sand-particles">
  <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
  <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
  <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
  <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
  <div class="particle" style="left: 50%; animation-delay: 0.5s;"></div>
  <div class="particle" style="left: 60%; animation-delay: 1.5s;"></div>
  <div class="particle" style="left: 70%; animation-delay: 2.5s;"></div>
  <div class="particle" style="left: 80%; animation-delay: 3.5s;"></div>
  <div class="particle" style="left: 90%; animation-delay: 0.8s;"></div>
  <div class="particle" style="left: 95%; animation-delay: 1.8s;"></div>
</div>

<div class="dune-container">
  
  <!-- Cinematic Header -->
  <header class="cinematic-header">
    <h1 class="name-title">SREE VARDHAN V</h1>
    <p class="spice-quote">"The spice must flow — and so does the code."</p>
  </header>

  <!-- Spice Stats -->
  <section class="spice-stats">
    <div class="stat-card">
      <div class="stat-icon">🌵</div>
      <div class="stat-label">Spice Harvested</div>
      <div class="stat-value">12.4K</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">⚙️</div>
      <div class="stat-label">Commits This Cycle</div>
      <div class="stat-value">527</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">🏗️</div>
      <div class="stat-label">Sietches Built</div>
      <div class="stat-value">15+</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">👁️</div>
      <div class="stat-label">Fremen Eyes</div>
      <div class="stat-value">∞</div>
    </div>
  </section>

  <!-- GitHub Stats Section -->
  <section class="github-stats">
    <h2 class="section-title" style="justify-content: center;">📊 SPICE HARVEST DATA</h2>
    <p style="color: var(--sand-light); opacity: 0.7; margin-bottom: 15px;">
      Real-time metrics from the desert of development
    </p>
    <div class="stats-row">
      <img src="https://github-readme-stats.vercel.app/api?username=vardhan23v&show_icons=true&theme=dark&bg_color=0A0A0A&title_color=D4A574&icon_color=C2622D&text_color=E8DCC4&border_color=D4A574&hide_border=true" alt="GitHub Stats" height="165"/>
      <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=vardhan23v&layout=compact&theme=dark&bg_color=0A0A0A&title_color=D4A574&text_color=E8DCC4&border_color=D4A574&hide_border=true" alt="Top Languages" height="165"/>
    </div>
    <div style="margin-top: 20px;">
      <img src="https://github-readme-streak-stats.herokuapp.com/?user=vardhan23v&theme=dark&background=0A0A0A&ring=D4A574&fire=C2622D&currStreakLabel=E8DCC4&sideNums=E8DCC4&sideLabels=E8DCC4&dates=E8DCC4&border=D4A574&hide_border=true" alt="GitHub Streak" height="170"/>
    </div>
  </section>

  <!-- Tech Still Suit -->
  <section class="still-suit">
    <h2 class="section-title">🛡️ TECH STILL SUIT</h2>
    <p style="color: var(--sand-light); opacity: 0.7; margin-bottom: 20px;">
      Every tool a Fremen needs to survive the desert of modern development
    </p>
    <div class="tech-grid">
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=react" alt="React">
        <span>React</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=nextjs" alt="Next.js">
        <span>Next.js</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=nodejs" alt="Node.js">
        <span>Node.js</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=typescript" alt="TypeScript">
        <span>TypeScript</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=python" alt="Python">
        <span>Python</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=mongodb" alt="MongoDB">
        <span>MongoDB</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=postgresql" alt="PostgreSQL">
        <span>PostgreSQL</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=docker" alt="Docker">
        <span>Docker</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=aws" alt="AWS">
        <span>AWS</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=git" alt="Git">
        <span>Git</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=tailwind" alt="Tailwind">
        <span>Tailwind</span>
      </div>
      <div class="tech-item">
        <img src="https://skillicons.dev/icons?i=prisma" alt="Prisma">
        <span>Prisma</span>
      </div>
    </div>
  </section>

  <!-- Projects - Sietches -->
  <section class="sietches">
    <h2 class="section-title">🏔️ SIETCHES (PROJECTS)</h2>
    
    <div class="sietch-card">
      <div class="sietch-info">
        <h3>✨ Extension AI — The Flagship Sietch</h3>
        <p>AI-powered Chrome extension generator from natural language prompts. The KWISATZ HADERACH of browser automation.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/extension-AI" class="sietch-link">Code</a>
        <a href="https://extension-ai-five.vercel.app" class="sietch-link">Live ↗</a>
      </div>
    </div>
    
    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🏦 LoanEase — Financial Stronghold</h3>
        <p>Multi-step loan application form with smooth UX. The economic engine of the sietch.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/LoanEase-Multi-Step-Form" class="sietch-link">Code</a>
        <a href="https://pro1-pied.vercel.app" class="sietch-link">Live ↗</a>
      </div>
    </div>
    
    <div class="sietch-card">
      <div class="sietch-info">
        <h3>⚡ Task Tracker SaaS — The Water Disciplinary</h3>
        <p>Enterprise task management platform. Every drop of productivity counted.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/task-tracker-saas" class="sietch-link">Code</a>
        <a href="https://task-tracker-rose-ten-60.vercel.app" class="sietch-link">Live ↗</a>
      </div>
    </div>
    
    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🎓 Campus Compass — Navigation Aid</h3>
        <p>Academic navigation and resource hub. Finding paths through the educational desert.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/campus-compass" class="sietch-link">Code</a>
        <a href="https://campus-compass-fawn.vercel.app" class="sietch-link">Live ↗</a>
      </div>
    </div>
    
    <div class="sietch-card">
      <div class="sietch-info">
        <h3>💼 CareerForge Pro — The Swordmaster</h3>
        <p>Career development and job matching platform. Forging the next generation of developers.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/career-forge-pro" class="sietch-link">Code</a>
        <a href="https://career-forge-pro-phi.vercel.app" class="sietch-link">Live ↗</a>
      </div>
    </div>
    
    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🤖 AI Code Reviewer — The Mentat</h3>
        <p>Machine learning-powered code analysis. The thinking machine of the development world.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/codereviewer" class="sietch-link">Code</a>
        <a href="https://codereviewer-eta.vercel.app" class="sietch-link">Live ↗</a>
      </div>
    </div>

    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🏏 HPL Auction — The Great Houses Arena</h3>
        <p>Real-time cricket auction platform with live bidding, purse management, and auctioneer controls.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/hpl-auction" class="sietch-link">Code</a>
        <a href="https://hpl-web-production.up.railway.app" class="sietch-link">Live ↗</a>
      </div>
    </div>

    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🛒 Apex Retail ERP — The Merchants' Guild</h3>
        <p>Retail POS and inventory platform with barcode scanning, GST invoices, stock audits, and RBAC.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/inventory-management" class="sietch-link">Code</a>
      </div>
    </div>

    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🧑‍💼 Dayflow HRMS — The Administrative Sietch</h3>
        <p>Employee directory, attendance, time off, payroll, and PDF payslips in one HR platform.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/Human-Resource-Management-System" class="sietch-link">Code</a>
      </div>
    </div>

    <div class="sietch-card">
      <div class="sietch-info">
        <h3>🎮 Logic Link — The Puzzle Chamber</h3>
        <p>A deterministic number-matching puzzle with solver validation and ten tuned difficulty levels.</p>
      </div>
      <div class="sietch-links">
        <a href="https://github.com/vardhan23v/logic-link" class="sietch-link">Code</a>
      </div>
    </div>
    
    <div style="text-align: center; margin-top: 20px;">
      <a href="https://github.com/vardhan23v?tab=repositories" style="color: var(--fremen-blue); font-size: 1rem;">
        🔍 Explore All Sietches →
      </a>
    </div>
  </section>

  <!-- Worm Path - Activity -->
  <section class="worm-path">
    <h2 class="section-title" style="justify-content: center;">🐛 THE SANDWORM PATH</h2>
    <p style="color: var(--sand-light); opacity: 0.7; margin-bottom: 15px;">
      My journey across the desert of code — each grain a commit, each ripple a contribution
    </p>
    <img src="https://github-readme-activity-graph.vercel.app/graph?username=vardhan23v&theme=dark&hide_border=true&bg_color=0A0A0A&color=D4A574&line=C2622D&point=00B4D8" alt="Contribution Graph">
  </section>

  <!-- Snake Animation -->
  <section class="snake-container">
    <h2 class="section-title" style="justify-content: center;">🐍 THE SANDWORM'S JOURNEY</h2>
    <p style="color: var(--sand-light); opacity: 0.7; margin-bottom: 15px;">
      Watching the contributions slither across the desert
    </p>
    <img src="https://raw.githubusercontent.com/vardhan23v/vardhan23v/output/github-contribution-grid-snake-dark.svg" width="100%" alt="Contribution Snake Animation"/>
  </section>

  <!-- Fremen Network -->
  <section class="fremen-network">
    <h2 class="section-title" style="justify-content: center;">🤝 FREMEN NETWORK</h2>
    <p style="color: var(--sand-light); opacity: 0.8; margin-bottom: 10px;">
      Open to joining forces for worthy causes
    </p>
    <div class="collab-list">
      <span class="collab-item">🌐 Full-Stack Applications</span>
      <span class="collab-item">🤖 AI-Integrated SaaS</span>
      <span class="collab-item">🔓 Open Source</span>
      <span class="collab-item">🏆 Hackathons</span>
      <span class="collab-item">🚀 Startup Ventures</span>
      <span class="collab-item">📚 Developer Education</span>
    </div>
  </section>

  <!-- Footer -->
  <footer class="dune-footer">
    <p class="blessing">"May thy knife chip and shatter"</p>
    <p style="color: var(--sand-light); opacity: 0.5; font-size: 0.8rem; margin-top: 10px;">
      — A Fremen Developer's Blessing
    </p>
    
    <div class="social-links">
      <a href="https://github.com/vardhan23v" class="social-link" title="GitHub">🐙</a>
      <a href="https://www.linkedin.com/in/vardhan-vs23012007/" class="social-link" title="LinkedIn">💼</a>
      <a href="mailto:23vvardhan@gmail.com" class="social-link" title="Email">✉️</a>
    </div>
    
    <p style="color: var(--spice-gold); opacity: 0.6; font-size: 0.75rem; margin-top: 30px;">
      ⚡ Built with the spice of determination ⚡
    </p>
  </footer>

</div>
