import React from 'react';
import { Card, CardContent, Typography, Button } from '@mui/material';

function InfoSection() {
  const openLink = (url) => {
    window.open(url, '_blank'); // '_blank' opens the link in a new tab
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', margin: '30px' }}>
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h5">What is DGA?</Typography>
          <Typography variant="body2">Learn about how DGAs are used in cybersecurity threats.</Typography>
          <Button variant="contained" color="primary" style={{ marginTop: '10px' }}
            onClick={() => openLink('https://en.wikipedia.org/wiki/Domain_generation_algorithm')}>Learn More</Button>
        </CardContent>
      </Card>
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h5">Resources</Typography>
          <Typography variant="body2">Explore further readings and external resources.</Typography>
          <Button variant="contained" color="primary" style={{ marginTop: '10px' }}
            onClick={() => openLink('https://www.cybereason.com/blog/what-are-domain-generation-algorithms-dga')}>Explore Resources</Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default InfoSection;
