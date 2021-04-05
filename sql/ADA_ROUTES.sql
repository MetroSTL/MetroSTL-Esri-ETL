select 
p.polytypeid as type,
m.lineabbr as route_abbr

from TRAPEZE.POLYGONS p
left join trapeze.routepolygonmap rp
on p.polyid = rp.polyid
left join trapeze.masterline m
on m.lineid = rp.lineid

where m.signid = 262
and p.polytypeid = 12

group by p.polytypeid,
            p.polyabbr,
            m.lineabbr
