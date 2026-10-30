<h1 align="center">Vardhan V</h1>

<p align="center">
  <strong>Full-Stack Developer · Generative AI Builder</strong><br/>
  I build production-ready web apps, real-time systems and AI-powered developer tools.
</p>

<p align="center">
  <a href="https://vardhan-v-portfilo.vercel.app/"><img src="https://img.shields.io/badge/Portfolio-1E3A5F?style=flat-square&logo=vercel&logoColor=white" alt="Portfolio"/></a>
  <a href="https://www.linkedin.com/in/vardhan-v23/"><img src="https://img.shields.io/badge/LinkedIn-1E3A5F?style=flat-square" alt="LinkedIn"/></a>
  <a href="https://github.com/vardhan23v?tab=repositories"><img src="https://img.shields.io/badge/Repositories-2B2F36?style=flat-square&logo=github&logoColor=white" alt="Repositories"/></a>
</p>

---

### About

Most student and small-team projects stop at a demo. I take mine to deployment: typed end to end,
backed by a real database, tested and live on the web.

My focus is where full-stack engineering meets generative AI: agent workflows, MCP tooling and
LLM features that hold up under real use, not only in a notebook.

- **Building:** AI-powered web apps, developer tools and real-time systems
- **Shipping on:** Vercel, Railway and AWS
- **Open to:** internships, collaborations and freelance work

### Tech Stack

**Languages**<br/>
![TypeScript](https://img.shields.io/badge/TypeScript-1E3A5F?style=flat-square&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-1E3A5F?style=flat-square&logo=javascript&logoColor=white)
![Python](https://img.shields.io/badge/Python-1E3A5F?style=flat-square&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-1E3A5F?style=flat-square&logo=openjdk&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-1E3A5F?style=flat-square&logo=mysql&logoColor=white)

**Frameworks**<br/>
![React](https://img.shields.io/badge/React-2B2F36?style=flat-square&logo=react&logoColor=22B8CF)
![Next.js](https://img.shields.io/badge/Next.js-2B2F36?style=flat-square&logo=nextdotjs&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-2B2F36?style=flat-square&logo=nodedotjs&logoColor=22B8CF)
![Express](https://img.shields.io/badge/Express-2B2F36?style=flat-square&logo=express&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-2B2F36?style=flat-square&logo=tailwindcss&logoColor=22B8CF)
![Prisma](https://img.shields.io/badge/Prisma-2B2F36?style=flat-square&logo=prisma&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.IO-2B2F36?style=flat-square&logo=socketdotio&logoColor=white)

**Data & Cloud**<br/>
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-1E3A5F?style=flat-square&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-1E3A5F?style=flat-square&logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-1E3A5F?style=flat-square&logo=mongodb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-1E3A5F?style=flat-square&logo=redis&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-1E3A5F?style=flat-square)
![Vercel](https://img.shields.io/badge/Vercel-1E3A5F?style=flat-square&logo=vercel&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-1E3A5F?style=flat-square&logo=docker&logoColor=white)

**AI / LLM**<br/>
![Gemini](https://img.shields.io/badge/Gemini-2B2F36?style=flat-square&logo=googlegemini&logoColor=22B8CF)
![OpenAI](https://img.shields.io/badge/OpenAI_API-2B2F36?style=flat-square)
![Groq](https://img.shields.io/badge/Groq_·_Llama-2B2F36?style=flat-square&logo=meta&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-2B2F36?style=flat-square)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-2B2F36?style=flat-square&logo=anthropic&logoColor=white)

### Selected Work

| Project | What it does | Stack |
| --- | --- | --- |
| [**Campus Compass**](https://github.com/vardhan23v/campus-compass) | College discovery and comparison for Indian students: search, filter, compare and review, with recommendations. | Next.js · PostgreSQL · Prisma · NextAuth |
| [**IPL Auction**](https://github.com/vardhan23v/ipl-auction) | Live multiplayer auction rooms. Share a code, claim franchises and bid in real time from any phone. | Next.js · Socket.IO · Prisma · MySQL |
| [**TrustLens AI**](https://github.com/vardhan23v/trustlens-ai) | Checks screenshots, messages and viral claims and returns an explainable, evidence-backed trust report. | Python · CrewAI · Gemini |
| [**ChitChain**](https://github.com/vardhan23v/chitchain) | A trust-minimised chit fund. The pot lives in a smart contract, and an AI risk engine prices collateral. | TypeScript · Smart contracts · AI agents |

### How I Build

A typical project of mine follows the same shape: a typed web client, an API layer that owns
validation and auth, a relational database, and AI services kept behind the server.

```mermaid
flowchart LR
    U[User] --> C[React / Next.js client]
    C -->|REST · WebSocket| A[API layer<br/>Node.js · Express · Next.js routes]
    A --> D[(PostgreSQL / MySQL<br/>via Prisma)]
    A --> R[(Redis cache)]
    A --> L[LLM services<br/>Gemini · Groq · OpenAI]
    L --> T[Agents & MCP tools]
    A --> H[Deploy<br/>Vercel · Railway · AWS]

    classDef navy fill:#1E3A5F,stroke:#1E3A5F,color:#ffffff;
    classDef cyan fill:#E6F7FA,stroke:#22B8CF,color:#2B2F36;
    class C,A navy;
    class D,R,L,T,H cyan;
```

---

<p align="center">
  <sub>
    Vardhan V ·
    <a href="https://vardhan-v-portfilo.vercel.app/">Portfolio</a> ·
    <a href="https://www.linkedin.com/in/vardhan-v23/">LinkedIn</a> ·
    <a href="https://github.com/vardhan23v">GitHub</a>
  </sub>
</p>
