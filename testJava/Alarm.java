public class Alarm {
    public static boolean setAlarm(boolean employed, boolean vacation) {
        if ((employed && vacation) || (!employed && vacation) || (!employed && !vacation))
            return false;
        else
            return true;
    }
}
