# Our Dataset

We used a dataset of the police uk (England, Wales, Northern Ireland). 

<img title="" src="file:///C:/Users/Pasca/OneDrive/Desktop/MLOPS/kirenz-mlops-semester/jupyter-book/assets/img/2021-12-15-17-19-20-image.png" alt="" data-align="center">

The API of the Police UK provides a rich data source of information, including: 

- Neighbourhood team members
- Upcoming events
- Street-level crime and outcome data
- Nearest police stations

URL: [Police API Documentation | data.police.uk](https://data.police.uk/docs/)

Out focuse is on the street-level crime and outcome data. So we use the data of stop an searches in different locations. The stop and searches returned in the API, like the crimes, are only an approximation of where the actual stop and searches occurred, they are **not** the exact locations. See [the about page](https://data.police.uk/about/#location-anonymisation) for more information about location anonymisation.

The Dataset ist divided in different forces. Each force is a country of the UK. Here a short overview of the forces: 

- metropolitan         

- merseyside      

- hames-valley       

- west-yorkshire      

- essex          

- south-yorkshire  

- kent             

- south-wales     

- btp             

- lancashire          

- hampshire          

- avon-and-somerset      

- west-midlands     

- hertfordshire      

- sussex               

- humberside             

- surrey           

- devon-and-cornwall     

- cleveland           

- staffordshire   

- cheshire          

- west-mercia           

- leicestershire         

- norfolk               

- nottinghamshire      

- northumbria            

- gwent               

- north-wales             

- bedfordshire        

- northamptonshire      

- suffolk               

- cambridgeshire        

- lincolnshire           

- derbyshire            

- dyfed-powys           

- city-of-london          

- north-yorkshire        

- dorset                

- cumbria                 

- warwickshire        

- durham                

- gloucestershire       

- wiltshire          
