const DashboardGrid = ({ children, className = '' }) => {
  return (
    <div
      className={`
        dashboard-grid
        grid
        grid-cols-1
        md:grid-cols-2
        xl:grid-cols-4
        gap-0
        mt-0
        ${className}
      `}
    >
      {children}
    </div>
  );
};

export default DashboardGrid;
