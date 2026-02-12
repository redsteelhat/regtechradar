export default function SettingsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <nav className="flex gap-4 mb-6 border-b pb-2">
        <a href="/settings/profile">Profile</a>
        <a href="/settings/billing">Billing</a>
        <a href="/settings/team">Team</a>
      </nav>
      {children}
    </div>
  );
}
