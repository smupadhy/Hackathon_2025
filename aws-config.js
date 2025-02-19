import Amplify from 'aws-amplify';

Amplify.configure({
  Auth: {
    region: 'ap-southeast-2', // e.g., us-east-1
    userPoolId: 'ap-southeast-2_bcsp9iJSr',
    userPoolWebClientId: '64da0c849cv69ucl87rskabcc2',
  },
});