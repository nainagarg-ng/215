import React from 'react';
import { Typography } from '@mui/material';

function Footer() {
  return (
    <footer style={{ textAlign: 'center', marginTop: '50px', padding: '20px', borderTop: '1px solid #eaeaea' }}>
      <Typography variant="body2" color="textSecondary">
        &copy; 2023 DGA Classifier. All rights reserved. version 3
      </Typography>
    </footer>
  );
}

export default Footer;
