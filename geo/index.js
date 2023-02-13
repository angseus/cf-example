import { Router } from 'itty-router'

// create a new router
const router = Router()

// geo information
router.get("/geo", (request, req) => {
  // debugging
  //console.log('\n### Request headers ###')
  //console.log(JSON.stringify(Object.fromEntries(request.headers)))
  //console.log('\n### CloudFlare headers ###')
  //console.log(JSON.stringify(request.cf))
  
  // geoip
  let ip      = request.headers.get('CF-Connecting-IP')
  let country = request.cf.country
  let asn     = request.cf.asn

  // redirect all non-SG users to CloudFlare DNS
  if (country != 'SG') {
    return Response.redirect('https://1.1.1.1', 301);
  } else {
    return new Response(`This is your client IP ${ip} and you are accessing this site from ${country} | ${asn}.`, { status: 200 })
  }
})

// fallback route
router.all("*", () => new Response("404, not found!", { status: 404 }))

// listener for all events
addEventListener('fetch', (e) => {
  e.respondWith(router.handle(e.request))
})
