import { Activity } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

import DashboardGrid from '@/components/dashboard/DashboardGrid';
import DashboardHero from '@/components/dashboard/DashboardHero';
import DashboardTile from '@/components/dashboard/DashboardTile';
import { useStaffDashboard } from '@/modules/staff/common/hooks/useStaffWorkspace';

export default function StaffDashboardPage({ config }) {
  const navigate = useNavigate();
  const { data } = useStaffDashboard(config);
  const profile = data?.profile || {};
  const summary = data?.summary || {};
  const Icon = config.primaryIcon || Activity;

  return (
    <>
      <DashboardHero
        badge={config.badge}
        title={`Welcome back${profile.full_name ? `, ${profile.full_name}` : ''}`}
        description={config.description}
        statusTitle={config.statusTitle}
        statusDescription={`${summary.pending_tasks ?? 0} pending tasks, ${summary.notifications ?? 0} notifications.`}
        icon={Icon}
      />

      <section className='-mt-2'>
        <DashboardGrid className='mt-0 gap-0'>
          {config.tiles.map((tile) => {
            const TileIcon = tile.icon;

            return (
              <DashboardTile
                key={tile.title}
                size={tile.size}
                variant={tile.variant}
                rounded='none'
                shadow
                onClick={() => navigate(tile.path)}
                className='group min-h-[180px] border border-white/10 p-5 hover:-translate-y-0'
              >
                <div className='relative z-10 flex h-full flex-col justify-between'>
                  <div className='flex items-start justify-between gap-4'>
                    <div>
                      <p className='text-xs uppercase tracking-[0.25em] text-white/80'>
                        {tile.title}
                      </p>

                      <h3 className='mt-2 text-xl font-semibold'>
                        {tile.subtitle}
                      </h3>
                    </div>

                    <div className='rounded-2xl bg-white/15 p-3 shadow-inner backdrop-blur-sm transition group-hover:scale-110'>
                      <TileIcon size={22} />
                    </div>
                  </div>

                  <div className='mt-4 flex items-center justify-between text-sm text-white/80'>
                    <span>Open workspace</span>

                    <span className='rounded-full bg-white/15 px-3 py-1 text-xs font-semibold'>
                      Quick access
                    </span>
                  </div>
                </div>
              </DashboardTile>
            );
          })}
        </DashboardGrid>
      </section>
    </>
  );
}
