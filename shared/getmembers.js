//takes year and chamber (senate or house) and gets every member that served that year
export function getMembersFromYear(chamber, year, data) {
    const congressNumberThatYear = Math.ceil((year - 1788) / 2);

    return data.filter(member => {
        let servedYear = false;
        member.terms.forEach(term => {
            if (term.chamber === chamber && term.congress === congressNumberThatYear) {
                servedYear = true;
            }
        })
        return servedYear;
    })
}
