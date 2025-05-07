        # gamma1 = atan2(p12[1]-p11[1], p12[0] - p11[0])
        # gamma2 = atan2(p22[1]-p21[1], p22[0] - p21[0])
        # gamma3 = atan2(p32[1]-p31[1], p32[0] - p31[0])
        
        # d1 = (self.pos_eff-p12).dot(array([-sin(gamma1),cos(gamma1),1]))
        # d2 = (self.pos_eff-p22).dot(array([-sin(gamma2),cos(gamma2),1]))
        # d3 = (self.pos_eff-p32).dot(array([-sin(gamma3),cos(gamma3),1]))
        
        # e1 = np.linalg.norm((p11-p10)*(p12-p10)/np.linalg.norm(p12-p10))
        # e2 = np.linalg.norm((p21-p20)*(p22-p20)/np.linalg.norm(p22-p20))
        # e3 = np.linalg.norm((p31-p30)*(p32-p30)/np.linalg.norm(p32-p30))
