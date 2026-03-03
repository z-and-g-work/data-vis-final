//takes year and chamber (senate or house) and gets every member that served that year
export function getMembersFromYear(chamber, year, data) {
    const congressNumberThatYear = Math.ceil((year - 1788) / 2);

    return data.filter(member => {
        let servedYear = false;
        member.terms.forEach(term => {
            if ((term.chamber === chamber || chamber === "Both") && term.congress === congressNumberThatYear) {
                servedYear = true;
            }
        })
        return servedYear;
    })
}

//returns a list of the years served in the house and senate for each congress member
export function getYearsServed(year, data) {
    const congressNumberThatYear = Math.ceil((year - 1788) / 2);
    return data.map(member => {
        let houseYears = 0;
        let senateYears = 0;

        member.terms.forEach(term => {
            if (term.congress <= congressNumberThatYear) {
                let yearsServedThatTerm = term.endYear - term.startYear;
                term.chamber === "Senate" ? senateYears += yearsServedThatTerm : houseYears += yearsServedThatTerm;
            }
        })

        //list position 1 is age,  2 is house, position 3 is senate
        return [member.name, year - member.yob, houseYears, senateYears]
    })
}