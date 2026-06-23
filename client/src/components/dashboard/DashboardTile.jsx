const sizes = {
  small: 'col-span-1 row-span-1',

  medium: 'col-span-1 row-span-2',

  // Same width as medium but twice the height
  tall: 'col-span-1 row-span-4',

  wide: 'col-span-2 row-span-1',

  large: 'col-span-2 row-span-2',

  full: 'col-span-full row-span-1',
};

const variants = {
  light: 'bg-surface-light dark:bg-surface-dark text-gray-900 dark:text-white',

  cases:
    'bg-gradient-to-br from-brand-primary via-blue-700 to-indigo-900 text-white',

  clients: 'bg-gradient-to-br from-emerald-500 to-teal-700 text-white',

  finance:
    'bg-gradient-to-br from-emerald-600 via-green-700 to-emerald-900 text-white',

  activities:
    'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white',

  messages:
    'bg-gradient-to-br from-blue-600 via-indigo-700 to-blue-900 text-white',

  billing:
    'bg-gradient-to-br from-emerald-800 via-green-900 to-emerald-950 text-white',

  lawyerContacts:
    'bg-gradient-to-br from-indigo-600 via-blue-700 to-slate-900 text-white',

  staff: 'bg-gradient-to-br from-violet-500 to-purple-700 text-white',

  revenue: 'bg-gradient-to-br from-amber-500 to-orange-600 text-white',

  hearings:
    'bg-gradient-to-br from-emerald-800 via-green-900 to-teal-950 text-white',

  notifications: 'bg-gradient-to-br from-slate-700 to-slate-900 text-white',

  tasks: 'bg-gradient-to-br from-cyan-500 to-sky-700 text-white',

  documents:
    'bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-950 text-white',

  ai: 'bg-gradient-to-br from-fuchsia-600 to-indigo-800 text-white',

  analytics: 'bg-gradient-to-br from-indigo-600 to-blue-900 text-white',

  courtroom:
    'bg-gradient-to-br from-cyan-400 via-sky-600 to-indigo-900 text-white',

  reports: 'bg-gradient-to-br from-green-600 to-emerald-800 text-white',

  calendar: 'bg-gradient-to-br from-sky-500 to-indigo-700 text-white',

  communication: 'bg-gradient-to-br from-cyan-600 to-blue-800 text-white',

  compliance: 'bg-gradient-to-br from-red-600 to-red-900 text-white',

  settings: 'bg-gradient-to-br from-slate-600 to-slate-800 text-white',

  glass: 'bg-white/10 backdrop-blur-lg text-white',
};

const DashboardTile = ({
  children,
  size = 'small',
  variant = 'light',
  className = '',
  rounded = '2xl',
  shadow = true,
  onClick,
}) => {
  const roundedClass =
    rounded === 'none' ? 'rounded-none' : `rounded-${rounded}`;

  const shadowClass = shadow
    ? 'shadow-[0_10px_30px_rgba(0,0,0,0.15)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.25)]'
    : 'shadow-none hover:shadow-none';

  const clickableClass = onClick ? 'cursor-pointer' : '';

  return (
    <div
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      className={`
        ${sizes[size] || sizes.small}
        ${variants[variant] || variants.light}

        ${clickableClass}

        relative
        overflow-hidden

        ${roundedClass}
        ${shadowClass}

        border border-white/10

        hover:-translate-y-1
        transition-all
        duration-300

        p-6

        ${className}
      `}
    >
      {children}
    </div>
  );
};

export default DashboardTile;
