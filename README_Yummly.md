**Yummly API Info**

https://developer.yummly.com

**Data Size**

2.1 M recipes

Recipe attributes:
[comment]: <> TODO: Finalise this.

**Yummly Attribution Requirements**

Whenever you display information obtained from the Yummly API to your users, 
you must give attribution to Yummly and the source of the recipe. 
The objects returned by the Get Recipe and Search Recipes API calls contain an attribution 
sub-object which consists of the following fields:

html: If your application uses HTML to display data to the users, you must include the contents of the html field
verbatim in a visible place near the data. You can ignore the other fields. You may not modify the HTML snippet.

url, text, logo: If your application is native (desktop or mobile) or otherwise doesn’t use HTML, 
you must display the text, the logo, and a link to the URL in a visible place near the data. 
Clicking this should open a browser on the url. You may not modify the URL, the link text, or the logo image.

source: The recipe objects returned by the Get Recipe API calls contain source attribution sub-object which 
consists of the following fields – sourceRecipeUrl, sourceSiteUrl, sourceDisplayName.
You must display the sourceDisplayName, and a link to either the sourceRecipeUrl and/or sourceSiteUrl in a
visible place near the data. Clicking this should open a browser on the url.
You may not modify the sourceRecipeUrl, sourceSiteUrl, or the sourceDisplayName. 
The elements of the matches array (i.e., matching recipes) in the Search Recipes API responses contain a 
sourceDisplayName field, and you must display its value in a visible place near the data, without modifying it.