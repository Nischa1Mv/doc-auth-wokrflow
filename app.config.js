import 'dotenv/config.js';

export default {
  expo: {
    name: "my-app",
    slug: "my-app",
    version: "1.0.0",
    extra: {
        BACKEND_URL: process.env.BACKEND_URL ,
    },
  },
};
