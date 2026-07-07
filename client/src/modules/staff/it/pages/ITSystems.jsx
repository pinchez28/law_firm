import { MonitorCog } from 'lucide-react';

import StaffWorkspacePage from '@/modules/staff/common/pages/StaffWorkspacePage';
import { staffRoleConfigs } from '@/modules/staff/common/config/staffRoleConfigs';

export default function ITSystems() {
  return (
    <StaffWorkspacePage
      config={staffRoleConfigs.it}
      endpoint='systems'
      responseKey='systems'
      title='Systems'
      description='System checks, support work, and technical operations.'
      icon={MonitorCog}
    />
  );
}
