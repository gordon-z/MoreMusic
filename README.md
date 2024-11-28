UPDATE: November 27 2024
Spotify has removed the recommendation endpoint from its Web API. This action destroyed the core functionality of my application, preventing it from generating recommendations using the Spotify API. Link to article here: https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api

--------------------------------------------------------------------------------------------------------
https://gordon-z.github.io/MoreMusic-frontend/

Frontend hosted on GitHub pages. Backend Django app and Postgres DB hosted on Render.

If link displays correctly but isn't able to login/create/delete recommendations, it's likely because application is hosted on Render's free tier, which automatically expires free applications after a certain time.

Frontend hosted on GitHub pages. Backend Django app and Postgres DB hosted on Render. 

If link displays correctly but isn't able to login/create/delete recommendations, it's likely because application is hosted on Render's free tier, which automatically expires free applications after a certain time.

## From Render: Your free instance will spin down with inactivity, which can delay requests by 50 seconds or more.

If requests take a long time to complete, this is why.
