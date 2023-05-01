using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Math;

namespace Dijkstra_s_Algorithm
{
    public class GFG
    {
        // graphta kaç nokta olduğunu belirtiyoruz
        public static int V = 10;

        // en kısa mesafe metodumuz dist dizisi ve spt dizisi içeriyor
        int minDistance(int[] dist, bool[] sptSet)
        {
            int min = int.MaxValue;
            int min_index = -1;

            for (int v=0;v<V; v++)
            {
                if (sptSet[v] == false && dist[v] <= min)
                {
                    min = dist[v];
                    min_index = v;
                }
            }
            return min_index;
        }

        void printSolution(int[] dist,int src)
        {
            Console.Write("\n-----Alanlar----- \t\t\t Kaynaktan uzaklık mesafesi\n");
            for (int i = 0; i < V; i++)
            {
                Console.Write( src+"-> kaynağından "+ i + "-> hedefine \t\t " + dist[i] + "\n");
            }
        }
        int kaynakuzaklık(int[] dist,int src)
        {
            int total=0;
            for (int i = 0; i < dist.Length; i++)
            {
                total+= dist[i];
            }
            Console.WriteLine(src + " kaynağından bütün hedeflere toplam uzaklık"+total);
            return total;

        }

        //elimizdeki graph'ı ve kaynak/başlagıç noktasını metodumuza yolluyoruz 
        public void dijkstra(int[,] graph, int src,out int toplamkısayol )
        {
            

            int[] dist = new int[V];

            bool[] sptSet = new bool[V];

            //bütün mesafeleri sonsuz olarak eşliyoruz ve sptsetlerini false olarak giriyoruz
            for (int i = 0; i < V; i++)
            {
                dist[i] = int.MaxValue;
                sptSet[i] = false;
                
            }

            dist[src] = 0;

            for (int count = 0; count < V; count++)
            {
                //0. indexten başlayıp düğüm noktası kadar dönüyor
                int u = minDistance(dist, sptSet);
                //Console.WriteLine(u);
                sptSet[u] = true;

                for (int v = 0; v < V; v++)
                {
                    if (!sptSet[v] && graph[u,v]!=0 && dist[u]!=int.MaxValue && dist[u] + graph[u, v] < dist[v])
                    {
                        dist[v] = dist[u] + graph[u, v];
                        
                    }
                }
            }


            printSolution(dist,src);//aralarındaki mesafeyi yazdırıyor


             toplamkısayol = kaynakuzaklık(dist,src);
             
            
            
        }

        

    }
    

    internal class Program
    {
        

        static void Main(string[] args)
        {


            /*double[,] kordinat= new double[,] 
            {
                { 0.0, 1.0 },
                { 2.0, 3.0 },
                { 4.0, 5.5 },
                { 6.0, 7.0 },
                { 8.0, 9.0 },
                { 10.0,11.0},
                { 12.0,50.0},
                { 7.0, 8.0 },
                { 4.0, 2.0 },
                { 5.0, 4.0 }
            };*/

            //lokasyonların kordinatlarını x y olacak şekilde yukarıda bulunan örnekteki  gibi  aşağıya giriniz.
            double[,] kordinat= new double[,] 
        {
                { 10.0, 1.0 },
                { 20.0, 3.0 },
                { 4.0, 5.5 },
                { 25.0, 25.0 },
                { 8.0, 9.0 },
                { 10.0,11.0},
                { 12.0,50.0},
                { 7.0, 8.0 },
                { 40.0, 2.0 },
                { 5.0, 4.0 }

        };
            int b = kordinat.GetLength(0);//kaç nokta olduğunun sayısı



            // birbirlerine olan uzaklıkların girilmesi için çok boyutlu diziyi oluşturuyoruz
            int[,] graph= new int[b,b] ;

            //toplam en kısa mesafeyi bulmak için dizi
            int[] toplam = new int[b];

            Uzaklık(kordinat, graph,b);
            //yaz(graph,b); graph eşitleme doğru çalışıyor mu diye çalıştırarak deneyebilirsiniz

        GFG t = new GFG();
            int toplamkısayol;
            
            // Function call

            for (int i = 0; i < b; i++)
            {
                t.dijkstra(graph, i,out toplamkısayol);
                toplam[i] = toplamkısayol;

            }
            tavsiye(toplam);

            
            
            
            Console.ReadLine();
        }

        private static void Uzaklık(double[,] kordi,int[,] graph,int b)
        {//noktalar arası mesafenin hesaplandığı metottur.
            for (int i = 0; i < b; i++)
            {
                for (int j = 0; j < b; j++)
                {
                    graph[i, j] = (int)(Sqrt( Pow(kordi[i, 0] - kordi[j, 0], 2) + (Pow(kordi[i, 1] - kordi[j, 1], 2)) ));
                }

            }
        }
        private static void yaz(int[,] graph,int b)
        {//uzaklık metodunun doğru çalışıp çalışmadığını kontrol etmek için metot
            for(int i = 0;i < b; i++)
            {
                for (int j = 0; j < b; j++)
                {
                    Console.Write(graph[i,j]+" ");
                }
                Console.WriteLine();
            }
        } 
        private static void tavsiye(int[] toplam)
        {
            int mesafe = int.MaxValue;
            int src = -1;
            for (int i = 0; i < toplam.Length; i++)
            {
                if (toplam[i] < mesafe)
                {
                    mesafe = toplam[i];
                    src = i;
                }
            }
            Console.ForegroundColor= ConsoleColor.Green;
           
            Console.Write("\n{0} kaynağından bütün lokasyonlara {1} birim yol gidilerek ulaşılabiliyor.\n" +
                "bu yüzden {0} kaynağının ana lojistik merkezi yapılması tavsiye edilmektedir.", src,mesafe);
            Console.ResetColor();
            
        }
    }
}
