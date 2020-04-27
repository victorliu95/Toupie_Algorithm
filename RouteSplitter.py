from Utils import *


def ClearExtraRouteInfo(steps):
    for step in steps:
        step.pop()
    return steps


def PrepareRouteForProcessing(steps):
    for step in steps:
        step.append(None)
    return steps


def SplitRoute(steps):
    steps = SplitRouteInDifferentDays(steps)
    return IncludeBreak(steps)


def IncludeBreak(steps):
    prevIndex = 0
    multipleDaysSchedule = []

    for i, step in enumerate(steps):
        if i > 0:
            if i == len(steps) - 1:
                multipleDaysSchedule.append(steps[prevIndex:i + 1])

            elif isinstance(step[departure], int) and step[departure] == startInMins:
                multipleDaysSchedule.append(steps[prevIndex:i])
                prevIndex = i

    for i, daySchedule in enumerate(multipleDaysSchedule):
        for j, step in enumerate(daySchedule):
            if isinstance(step[arrival], int) and step[arrival] > breakHourInMins and j > 0:
                step[notes] = lunchBreak
                multipleDaysSchedule[i] = AddBreakTimeDifference(daySchedule, breakDurationInMins, j)
                
                break
            elif isinstance(step[arrival], int) and j == 0:
                step[arrival] = step[arrival] + breakDurationInMins

    result = []
    for i, daySchedule in enumerate(multipleDaysSchedule):
        for j, step in enumerate(daySchedule):
            result.append(step)

    return result


def AddBreakTimeDifference(steps, breakDurationInMins, indexExceeding):
    for step in steps[indexExceeding:]:
        if isinstance(step[arrival], int):
            step[arrival] = step[arrival] + breakDurationInMins
        if isinstance(step[departure], int):
            step[departure] = step[departure] + breakDurationInMins
    return steps


def SplitRouteInDifferentDays(steps):
    for i, step in enumerate(steps):
        if isinstance(step[arrival], int) and step[arrival] > endInMins:
            return GetUpdatedRoute(steps, i, True)
        if isinstance(step[departure], int) and step[departure] > endInMins:
            return GetUpdatedRoute(steps, i, False)
    return steps


def GetUpdatedRoute(steps, indexExceeding, isExceedingInArrival):
    arrival = 3
    departure = 4

    if isExceedingInArrival:
        oldDepartureInMins = steps[indexExceeding - 1][departure]
        differenceInMins = oldDepartureInMins - startInMins

        steps[indexExceeding - 1][departure] = startInMins
        steps[indexExceeding][arrival] = SetNewTimeInMins(steps[indexExceeding][arrival], differenceInMins)
        steps[indexExceeding][departure] = SetNewTimeInMins(steps[indexExceeding][departure], differenceInMins)

    else:  # isExceedingInDeparture
        oldDepartureInMins = steps[indexExceeding][departure]
        differenceInMins = oldDepartureInMins - startInMins

        steps[indexExceeding][departure] = startInMins

    for step in steps[indexExceeding + 1:]:
        step[arrival] = SetNewTimeInMins(step[arrival], differenceInMins)
        step[departure] = SetNewTimeInMins(step[departure], differenceInMins)

    return steps


def SetNewTimeInMins(oldValue, differenceInMins):
    if isinstance(oldValue, int):
        return oldValue - differenceInMins
    else:
        return oldValue

def InsertBreakRows(steps):
    steps = InsertLunchBreakRows(steps)
    return InsertDaySeparationRows(steps)

def InsertLunchBreakRows(steps):
    result = []
    for i, step in enumerate(steps):
        if isinstance(step[arrival], int) and step[notes] == lunchBreak:
            # steps.insert(i, ["Break", "", "", int(breakHourInMins), int(breakHourInMins + breakDurationInMins), "", ""])
            result.append(["Break", "", "", int(breakHourInMins), int(breakHourInMins + breakDurationInMins), "", ""])
        
        result.append(step)
        
    return result

def InsertDaySeparationRows(steps):
    for i, step in enumerate(steps):
        if isinstance(step[arrival], int) and step[departure] == startInMins and i > 0:
            steps.insert(i, step.copy())
            steps[i][departure] = 'None'
            steps[i+1][arrival] = 'None'
            steps.insert(i+1, ["", "", "", "", "", "", ""])
            break
    return steps


# RouteFormatter

def FormatRouteTimesInHours(steps):
    for i, step in enumerate(steps):
        if isinstance(step[arrival], int):
            step[arrival] = ConvertSecToHoursMin(step[arrival])
            # if step[notes] == lunchBreak:
            #     step[arrival] = step[arrival] + " (*)"

        if isinstance(step[departure], int):
            step[departure] = ConvertSecToHoursMin(step[departure])

    return steps


# file scope variables

startHour = 8
endHour = 17
maxHour = 24
startInMins = startHour * 60
endInMins = endHour * 60
maxInMins = maxHour * 60

breakHour = 12.5
breakHourInMins = breakHour * 60
breakDuration = 1
breakDurationInMins = breakDuration * 60

arrival = 3
departure = 4
notes = 6

lunchBreak = "lunchBreak"
