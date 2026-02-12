export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen">
      {/* Sidebar + main content — shared Navbar/Sidebar components TODO */}
      <aside className="fixed left-0 top-0 h-full w-56 border-r bg-gray-50 p-4">
        <p className="font-medium">RegTech Radar</p>
        <nav className="mt-4 space-y-1 text-sm">
          <a href="/feed" className="block">Feed</a>
          <a href="/search" className="block">Search</a>
          <a href="/alerts" className="block">Alerts</a>
          <a href="/impact" className="block">Impact</a>
          <a href="/timeline" className="block">Timeline</a>
          <a href="/settings/profile" className="block">Settings</a>
        </nav>
      </aside>
      <main className="pl-56 p-6">{children}</main>
    </div>
  );
}
