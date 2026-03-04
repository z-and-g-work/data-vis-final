---
owner: "gabe"
users: {"gabe"}
---

Need to put down some ideas and at this point i am spamming the group chat.

## api
we will be using exclusivly api.congress.gov
every limitation that me and zach where talking about was directly solved by a get from /member/{biogiudeId} 
(ideally with some local caching in order to not get the same information from the api a million times. who wants a technical achievement???) 

i think that this information should be gotten a single time for all of the information that is not really going to change. this is something that i would like to keep up to date by itself - i think i could just set up a cron job to update all the information, post it to the repo, and have a github action to post it to a data base that will be just this information. this is something that i will likly be doing on the side as this is not too important to us at this. i will handle the retreval and processing of this information. I will probably definatly be using python for this.
#### Here is the process to gather this information: 
1. query /members
this will get all of the general information on members currently active. this does not have to be hit very often

2. process this information
we want to get the current members that are activly serving. this WILL prove to be a harder task than i am outlining it to be here. the problem is that this is going to require extra work because of the house? (i honestly forget which) only seems to be serving the years that they started and not currently. this being inefficeint is not really my problem tho. this is only going to be run once for the sake of this project. all the information that we have to keep (or ig find if it is not there) is the house / sen and the bioguideid (really useful! you see soon enough...)

3. use the bioguideid for a get on /member/{bioguideId}
this is where we will be getting almost all of out information
the most pertinent of which are 
- the year of birth 
- terms
{
      "chamber": "Senate",
      "congress": 116,
      "endYear": 2021,
      "memberType": "Senator",
      "startYear": 2019,
      "stateCode": "VT",
      "stateName": "Vermont"
    }
  ],
we ofc will be using the year of birth - but we can use the information from the terms for the following: 


below is a real example off a random guy. my fault for doxing you XoXoXo
``` json
{
  "bioguideId": "L000174",
  "birthYear": "1940",
  "cosponsoredLegislation": {
    "count": 1,
    "url": "https://api.congress.gov/v3/member/L000174/cosponsored-legislation\""
  },
  "depiction": {
    "attribution": "<a href=\"\\&quot;https://www.senate.gov/artandhistory/history/common/generic/Photo_Collection_of_the_Senate_Historical_Office.htm\\&quot;\">Courtesy U.S. Senate Historical Office</a>",
    "imageUrl": "https://www.congress.gov/img/member/l000174_200.jpg"
  },
  "directOrderName": "Patrick J. Leahy",
  "firstName": "Patrick",
  "honorificName": "Mr.",
  "invertedOrderName": "Leahy, Patrick J.",
  "lastname": "Leahy",
  "leadership": [
    {
      "congress": 113,
      "type": "President Pro Tempore"
    }
  ],
  "partyHistory": [
    {
      "partyAbbreviation": "D",
      "partyName": "Democrat",
      "startYear": 1975
    }
  ],
  "sponsoredLegislation": {
    "count": 1768,
    "url": "https://api.congress.gov/v3/member/L000174/sponsored-legislation"
  },
  "state": "Vermont",
  "terms": [
    {
      "chamber": "Senate",
      "congress": 116,
      "endYear": 2021,
      "memberType": "Senator",
      "startYear": 2019,
      "stateCode": "VT",
      "stateName": "Vermont"
    }
  ],
  "updateDate": "2022-11-07T13:42:19Z"
}
```
DO NOT GET SCARED ABOUT THE UPDATEDATE. its fine - this is just old. not talking out of trama or anything like that 
