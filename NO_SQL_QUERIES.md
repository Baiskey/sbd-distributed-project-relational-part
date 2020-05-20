business queries

1. Return list of people with information how much children they have

`db.person.aggregate([
   {
      $project: {
          name:1,
          surname: 2,
          city:3,
          gender:4,
          birthday: 5,
          children: {$cond: {if: {$isArray: "$children"}, then: {$size: "$children"}, else: "NA"}}
      }
   }
] )`



2. Return list of people with their homes and calculate how much days has passed since their moved

`db.person.aggregate(
[{
    $lookup: {
      from: 'address',
      localField: 'residence_id',
      foreignField: 'id',
      as: 'property'
}
}, {
    $unwind: {
        path: "$property",
        preserveNullAndEmptyArrays: false
    }
}, {
    $project: {
        pesel: 1,
        name: 1,
        surname: 1,
        moved_date: "$residence_moved_date",
        dayssince: {
            $divide: [{
                $subtract: [new Date(), {
                    $dateFromString: {
                        dateString: "$residence_moved_date"
                    }
                }]
            }, 1000 * 60 * 60 * 24]
        }
    }
}]
)`

3. Return list of PESELs of spouses and calculate how much time has passed between their marrage and moving in to flat

