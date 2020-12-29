using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Forms;
using System.Net;
using System.Collections.Generic;
using System;
using System.Diagnostics;
using System.Linq;
using System.Net.NetworkInformation;
using System.Reflection;
using System.Windows.Threading;

namespace Tor
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {

        public static List<IPAddress> arr_ip = new List<IPAddress>();
        public static int count_th;
        public static int split_cnt;


        public MainWindow()
        {
            InitializeComponent();
            Progress_btn.Visibility = Visibility.Hidden;

        }


        private void IPSCAN_Click(object sender, RoutedEventArgs e)
        {
            arr_ip.Clear();
            string srcIP = "192.168.1.1";
            string dstIP = "192.168.1.100";
            int src_idx = Int32.Parse(srcIP.Substring(10));
            int dst_idx = Int32.Parse(dstIP.Substring(10));

            int IP_range = dst_idx - src_idx + 1;
            double term_idx = 0;

            if (IP_range <= 10)
            {
                split_cnt = 1;
                progressBar1.Maximum = split_cnt;
                term_idx = IP_range / split_cnt;

                Run_Thread(srcIP, src_idx, dst_idx, term_idx, split_cnt);
            }
            else if (IP_range < 30)
            {
                split_cnt = 2;
                progressBar1.Maximum = split_cnt;
                term_idx = IP_range / split_cnt;
                Run_Thread(srcIP, src_idx, dst_idx, term_idx, split_cnt);
            }
            else if (IP_range <= 50)
            {
                split_cnt = 3;
                progressBar1.Maximum = split_cnt;
                term_idx = IP_range / split_cnt;
                Run_Thread(srcIP, src_idx, dst_idx, term_idx, split_cnt);
            }
            else
            {
                split_cnt = 4;
                progressBar1.Maximum = split_cnt;
                term_idx = IP_range / split_cnt;
                Run_Thread(srcIP, src_idx, dst_idx, term_idx, split_cnt);
            }

            //progressBar1.Value = 100;


            //Thread tn = new Thread(()=> IP_SCAN("192.168.1.1", "192.168.1.50"));
            //tn.IsBackground = true;
            //tn.Start();

            Debug.WriteLine("IPSCAN END");

            //IP_SCAN("192.168.1.1","192.168.1.50");
        }

        public void Run_Thread(string srcIP, int src_idx, int dst_idx, double term_idx, int split_cnt)
        {
            int[] arr_idx = new int[split_cnt + 1];

            /*            MessageBox.Show(term_idx.ToString());
            */
            arr_idx[0] = src_idx;
            arr_idx[split_cnt] = dst_idx;

            for (int i = 1; i < split_cnt; i++)
            {
                arr_idx[i] = arr_idx[i - 1] + (int)term_idx;

                // Debug.WriteLine(srcIP.Substring(0, 10) + arr_idx[i - 1].ToString(), srcIP.Substring(0, 10) + arr_idx[i].ToString());
                // new Thread(() => IP_SCAN(srcIP.Substring(0, 10) + arr_idx[i - 1].ToString(), srcIP.Substring(0, 10) + arr_idx[i].ToString(), i)).Start();
                //Debug.WriteLine(arr_idx[i]); 
            }

            for (int i = 0; i < split_cnt; i++)
            {
                Debug.WriteLine(arr_idx[i]);
            }


            for (int i = 1; i < split_cnt + 1; i++)
            {
                new Thread(() => IP_SCAN(srcIP.Substring(0, 10) + arr_idx[i - 1].ToString(), srcIP.Substring(0, 10) + arr_idx[i].ToString(), i, split_cnt)).Start();
                Thread.Sleep(10);
            }
        }

        public void IP_SCAN(String arg1, String arg2, int idx, int split_cnt)
        {

            var startIp = IPAddress.Parse(arg1);
            var endIp = IPAddress.Parse(arg2);
            IPAddress address = startIp;


            while (true)
            {

                Ping pingsender = new Ping();
                PingReply reply = pingsender.Send(address, 2);
                String logMessage = address.ToString();
                Debug.WriteLine(idx + " : 아이피 스캔 시작 IP : " + logMessage);
                string addr;
                string features;
                var sort_ip = arr_ip;

                if (reply.Status == IPStatus.Success)
                {
                    //ConnectionVO item_ip = new ConnectionVO(No_1.ToString(), "-", "-", "-", "-", "-");

                    //// Func는 반환값이 있는 메소드를 참조하는 델리게이트 변수
                    //// Action은 반환값이 없는 메소드를 참조하는 델리게이트 변수

                    //Action action = () => connectionListView.Items.Add(item_ip);
                    //Action action2 = () => connectionListView.ScrollIntoView(connectionListView.Items[connectionListView.Items.Count - 1]);

                    //connectionListView.Dispatcher.Invoke(action);
                    //connectionListView.Dispatcher.Invoke(action2);

                    //No_1++;

                    Debug.WriteLine(idx + " : success : " + address.ToString());

                    arr_ip.Add(address);
                }

                var bytes = address.GetAddressBytes();

                if (++bytes[3] == 0)
                    if (++bytes[2] == 0)
                        if (++bytes[1] == 0)
                            ++bytes[0];


                if (address.Equals(endIp))
                {
                    sort_ip = arr_ip.Distinct().OrderBy(j => new Version(j.ToString())).ToList();
                    //System.Windows.MessageBox.Show(count_th.ToString());
                    count_th += 1;


                    for (int i = 0; i < sort_ip.Count; i++)
                    {
                        Debug.WriteLine(idx + " : 스캔된 아이피 : " + sort_ip[i]);
                    }
                    //Thread.Sleep(10);
                    if (!this.Dispatcher.CheckAccess())
                    {
                        this.Dispatcher.Invoke(new Action(delegate ()
                        {
                            progressBar1.Value = count_th;
                            if (count_th== split_cnt) {
                                Progress_btn.Visibility = Visibility.Visible;
                            }
                        }));

                    } 
                    break;

                        //MessageBox.Show("IP SCAN 종료");
                    }


                    address = new IPAddress(bytes);

                }

            
        }

        public void Progress_Click(object sender, RoutedEventArgs e)
        {
            
            

              


            
        }
    }
    } 

