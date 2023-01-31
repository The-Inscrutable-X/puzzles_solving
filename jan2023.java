package a1;
import java.lang.Math;
import java.util.Scanner;
import java.util.Arrays;
public class jan2023{
    public static void main (String[] args) {
        brute(100);
        Scanner input = new Scanner(System.in);
        while (true) {
            int[] startingCorners = new int[4];
            for (int i = 0; i < 4; i++) {
                startingCorners[i] = input.nextInt();
            }
            print(Arrays.toString(findFromCorners(startingCorners)));
        }
    }
    static void print(Object input) {
        System.out.println(input);
    }

    public static void brute(int maxCorner) {
        int[][] max_corners = new int[30][5];
        for (int a = 0; a < maxCorner; a++) {
            for (int b = 0; b < maxCorner; b++) {
                for (int c = 0; c < maxCorner; c++) {
                    for (int d = 0; d < maxCorner; d++) {

                        int[] inputer = new int[4];
                        inputer[0] = a;
                        inputer[1] = b;
                        inputer[2] = c;
                        inputer[3] = d;
                        int[] data = findFromCorners(inputer);
                    }
                }
//                print("Pow!");
            }
//            print("DAngo!!");
        }
        print("FINGOOO!!!");
    }
    public static int[] findFromCorners (int[] startingCorners) {
        int[] telemetry = new int[4+1];
        for (int i = 0; i < startingCorners.length; i++) {
            telemetry[i] = startingCorners[i];
        }
        int[] corners = new int[4];
        for (int i = 0; i < startingCorners.length; i++) {
            corners[i] = startingCorners[i];
        }
        boolean working = true;
        int totalSquares = 1;
        int[] baseCase = new int[4];
        while (working) {
            if (Arrays.equals(baseCase, corners)) {break;}
            int temp = corners[0];
            corners[0] = Math.abs(corners[0] - corners[1]);
            corners[1] = Math.abs(corners[1] - corners[2]);
            corners[2] = Math.abs(corners[2] - corners[3]);
            corners[3] = Math.abs(corners[3] - temp);
            ++totalSquares;
//            print(totalSquares);
//            print(Arrays.toString(corners));
        }
        telemetry[4] = totalSquares;
        return telemetry;
    }
}
