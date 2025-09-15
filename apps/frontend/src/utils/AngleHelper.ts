export default class AngleHelper {
    public static angleBetweenPointsInDegrees(x1: number, y1: number, x2: number, y2: number) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        const radians = Math.atan2(dy, dx);
        const degrees = radians * (180 / Math.PI);
        return (degrees + 360) % 360;
    }

    public static angleBetweenPointsInRadians(x1: number, y1: number, x2: number, y2: number) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        const radians = Math.atan2(dy, dx) + 2 * Math.PI;
        return radians % (2 * Math.PI);
    }

    public static radianToDegree(radians: number) {
        return radians * (180 / Math.PI);
    }

    public static degreeToRadian(degrees: number) {
        return degrees * (Math.PI / 180);
    }
}