"use client"
import Link from "next/link";
import ButtonCustom from "./ButtonCustom";
import { useEffect, useState } from "react";
import { FetchUser, User } from "../utils/fetchUser";

export default function Topbar() {
  const api_url = process.env.NEXT_PUBLIC_API_URL
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    async function getUser() {
      const fetchResult = await FetchUser()
      setUser(fetchResult)
    }
    getUser()

    console.log(user)
  }, [])

  return (
    <div className="bg-topbar-bg top-0 inset-x-0 z-10 grid grid-cols-2 items-center px-6 py-3">
      <div>
        <Link href="/">osu!similarity</Link>
      </div>
      <div className="flex justify-end">
        {!user && (

          <ButtonCustom variant="osu" text="Sign up with osu!" onClick={() => { window.location.href = `${api_url}/api/login/` }} />
        )}
      </div>
    </div>
  );
}
