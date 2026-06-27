<template>
  <div class="public-shell">
    <header class="site-header">
      <RouterLink class="brand" to="/">AI Agent Intelligence</RouterLink>
      <nav class="nav">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/briefs">每日简报</RouterLink>
        <RouterLink to="/search">搜索问答</RouterLink>
        <RouterLink to="/login">管理入口</RouterLink>
      </nav>
    </header>
    <main class="site-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.public-shell {
  min-height: 100vh;
  background: #f6f8fb;
  color: #1f2937;
}

.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 18px 32px;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}

.brand {
  color: #111827;
  font-size: 20px;
  font-weight: 700;
  text-decoration: none;
}

.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.nav a {
  color: #4b5563;
  text-decoration: none;
}

.nav a.router-link-active {
  color: #2563eb;
}

.site-main {
  max-width: 1120px;
  margin: 0 auto;
  padding: 28px 20px 48px;
}
</style>
